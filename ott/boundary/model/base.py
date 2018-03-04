from gtfsdb.model.base import Base as GtfsdbBase
from ott.utils import geo_db_utils

import logging
log = logging.getLogger(__file__)


class Base(GtfsdbBase):

    def intersect(self, point):
        return geo_db_utils.does_point_intersect_geom(point, self.geom)

    def distance(self, point):
        return geo_db_utils.point_to_geom_distance(point, self.geom)

