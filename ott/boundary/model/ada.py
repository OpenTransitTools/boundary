import datetime

from sqlalchemy import Column, Sequence
from sqlalchemy.types import Date, Integer, String
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.sql.functions import func

from gtfsdb import config
from gtfsdb.model.base import Base as GtfsdbBase
from ott.boundary.model.base import Base

import logging
log = logging.getLogger(__file__)


class Ada(GtfsdbBase, Base):
    """
    The Americans with Disabilities Act (https://www.ada.gov) requires transit agencies to provide
    complementary paratransit service to destinations within 3/4 mile of all fixed routes.
    :see: https://en.wikipedia.org/wiki/Paratransit#Americans_with_Disabilities_Act_of_1990

    This class will calculate and represent a Paratransit (or ADA) boundary against all active routes.

    NOTE: to load this table, you need both a geospaitial db (postgis) and the --create_boundaries cmd-line parameter
    """
    datasource = config.DATASOURCE_DERIVED

    __tablename__ = 'ada'

    #geometry_type = 'MULTIPOLYGON'

    def __init__(self, name):
        self.name = name
        self.start_date = self.end_date = datetime.datetime.now()

    @classmethod
    def post_process(cls, db, **kwargs):
        if hasattr(cls, 'geom'):
            from gtfsdb.model.route import Route
            db.prep_an_orm_class(Route)

            log.debug('{0}.post_process'.format(cls.__name__))
            ada = cls(name='ADA Boundary')

            # 3960 is the number of feet in 3/4 of a mile this is the size of the buffer around routes that
            # is be generated for the ada boundary
            # todo: make this value configurable ... and maybe metric ...
            # todo: the following doesn't work ... too big of a buffer ... so

            # the buffer values of 0.0036 is not scientifically determined ... rather it looks good on a limited case
            geom = db.session.query(
                func.ST_ExteriorRing(
                    func.ST_Union(
                        Route.geom.ST_Buffer(0.011025, 'quad_segs=50')
                    )
                )
            )
            geom = func.ST_MakePolygon(geom)

            # TODO: clip the ADA geom against the District geom ... no ADA outside legal transit district
            ada.geom = geom

            db.session.add(ada)
            db.session.commit()
            db.session.close()
