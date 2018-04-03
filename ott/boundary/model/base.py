from sqlalchemy import Column, Sequence
from sqlalchemy.orm.session import Session
from sqlalchemy.types import Date, Integer, String
from sqlalchemy.orm import deferred, relationship
from geoalchemy2 import Geometry

from ott.utils import geo_utils
from ott.utils import geo_db_utils
from ott.utils import num_utils


import logging
log = logging.getLogger(__file__)


class Base(object):

    id = Column(Integer, Sequence(None, optional=True), primary_key=True, nullable=True)
    name = Column(String(255), nullable=False)
    start_date = Column(Date, index=True, nullable=False)
    end_date = Column(Date, index=True, nullable=False)

    session = None  # assumed to get set (as an @property) by way of Base in gtfsdb project
    geometry_type = 'POLYGON'

    def is_within(self, point):
        ret_val = geo_db_utils.does_point_intersect_geom(self.session, point, self.geom)
        log.debug('does point {} intersect geom {} == {}'.format(point, self.name, ret_val))
        return ret_val

    def is_within_xy(self, x, y):
        point = geo_utils.make_point(x, y)
        return self.is_within(point)

    def distance(self, point, units='feet+inches'):
        degrees = geo_db_utils.point_to_geom_distance(self.session, point, self.geom)
        ret_val = degrees
        if units != 'degrees':
            if units == 'meters':
                ret_val = num_utils.degrees_to_meters(degrees)
            else:
                ret_val = num_utils.degrees_to_feet(degrees)

        log.debug('distance of point {} from geom {} == {}'.format(point, self.name, ret_val))
        return ret_val

    @classmethod
    def load(cls, db, **kwargs):
        if hasattr(cls, 'geom'):
            log.debug('{0}.load (loaded later in post_process)'.format(cls.__name__))

    @classmethod
    def add_geometry_column(cls):
        if not hasattr(cls, 'geom'):
            log.debug('{0}.add geom column'.format(cls.__name__))
            cls.geom = deferred(Column(Geometry(cls.geometry_type)))

    @classmethod
    def read_shp(cls, shp_dir_path):
        r = geo_utils.read_shp(shp_dir_path)
        return r

