import datetime

from sqlalchemy import Column, Sequence
from sqlalchemy.types import Date, Integer, String
from sqlalchemy.sql.functions import func

from gtfsdb import config
from gtfsdb.model.base import Base as GtfsdbBase

from ott.boundary.model.base import Base

import logging
log = logging.getLogger(__file__)


class District(GtfsdbBase, Base):
    """
    Service District bounding geometry
    can be configured to load a service district shape
    or will calculate a boundary based on the extents of the route geometries

    NOTE: to load this table, you need both a geospaitial db (postgis) and the --create_boundaries cmd-line parameter
    """
    datasource = config.DATASOURCE_DERIVED

    __tablename__ = 'district'

    def __init__(self, name):
        self.name = name
        self.start_date = self.end_date = datetime.datetime.now()

    @classmethod
    def post_process(cls, db, **kwargs):
        if hasattr(cls, 'geom'):
            log.debug('{0}.post_process'.format(cls.__name__))
            district = cls(name='District Boundary')

            # make / grab the geometry
            geom = None
            if True:  # config.district_boundary_shp_file:
                geom = cls.shp_file_boundary()
            if geom is None:
                geom = cls.calculated_boundary(db)
            district.geom = geom

            db.session.add(district)
            db.session.commit()
            db.session.close()

    @classmethod
    def calculated_boundary(cls, db):
        """
        # Fill holes in buffered district map
        # https://geospatial.commons.gc.cuny.edu/2013/11/04/filling-in-holes-with-postgis/
        # https://postgis.net/docs/ST_ExteriorRing.html
        # NOTE ST_ExteriorRing won't work with MULTIPOLYGONS
        # https://postgis.net/docs/ST_Buffer.html
        """
        from gtfsdb.model.route import Route
        db.prep_an_orm_class(Route)

        log.info('calculating the service district boundary from an abitrary buffer / extent on routes')
        geom = db.session.query(
            func.ST_ExteriorRing(
                func.ST_Union(
                    Route.geom.ST_Buffer(0.0085, 'quad_segs=4 endcap=square join=mitre mitre_limit=1.0'))))
        ret_val = func.ST_MakePolygon(geom)
        return ret_val

    @classmethod
    def shp_file_boundary(cls):
        """
        load the boundary geometry from a .shp file
        """
        ret_val = None
        if ret_val is None:
            log.warn('was not able to grab a district boundary from a .shp file')
        return ret_val

