from sqlalchemy import Column, Sequence
from sqlalchemy.orm import deferred, relationship
from geoalchemy2 import Geometry

from ott.utils import geo_db_utils

import logging
log = logging.getLogger(__file__)


class Base(object):

    def intersect(self, point):
        return geo_db_utils.does_point_intersect_geom(point, self.geom)

    def distance(self, point):
        return geo_db_utils.point_to_geom_distance(point, self.geom)

    @classmethod
    def add_geometry_column(cls):
        if not hasattr(cls, 'geom'):
            log.debug('{0}.add geom column'.format(cls.__name__))
            cls.geom = deferred(Column(Geometry('POLYGON')))
