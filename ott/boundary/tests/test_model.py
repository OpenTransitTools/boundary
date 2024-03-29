import os
import datetime
import tempfile

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from gtfsdb import *  # noqa
from gtfsdb.api import database_load

from ott.boundary.model.ada import Ada
from ott.boundary.model.district import District

from ott.utils import file_utils
from ott.utils import geo_utils

import logging
log = logging.getLogger(__name__)


class BasicModelTests(object):

    try:
        path = resource_filename('gtfsdb', 'tests')
        gtfs_file = 'file:///{0}'.format(os.path.join(path, 'large-sample-feed.zip'))
        db_file = tempfile.mkstemp()[1]
        url = 'sqlite:///{0}'.format(db_file)
        db = database_load(gtfs_file, url=url)
        log.debug("DATABASE TMP FILE: {0}".format(db_file))
    except Exception as e:
        log.warning(e)
        log.warning("couldn't make the BasicModelTests object for some reason")

    def get_first(self):
        try:
            self._first
        except AttributeError:
            if hasattr(self, 'model'):
                self._first = self.db.session.query(self.model).first()
                return self._first

    def test_entity(self):
        if hasattr(self, 'model'):
            for r in self.db.session.query(self.model).limit(5):
                self.assert_(isinstance(r, self.model))


class TestRouteDirection(unittest.TestCase, BasicModelTests):
    model = Ada


def test_shp_file(file_name="tm_boundary"):
    dir = file_utils.get_file_dir(__file__)
    file_path = os.path.join(dir, 'data', file_name)
    shp = District.read_shp(file_path)
    geo = shp.shapes()
    print(shp, 'len =', len(geo))
    pt = geo[0].points[0]
    print(geo_utils.to_lon_lat_tuple(pt))


def test_boundaries():
    """
    run by main, will test boundary intersection in established Geo database, with existing populated boundary tables
    """
    from ott.utils import geo_utils

    point_in_both  = geo_utils.make_point(lat=45.51, lon=-122.68)
    point_district = geo_utils.make_point(lat=45.51, lon=-122.67)
    point_far_away = geo_utils.make_point(lat=45.5,  lon=-122.5)

    # with db connection, get ADA and District boundaries
    db = "#TODO ... was db_utils.db_args_gtfsdb()"
    ada = db.session.query(Ada).first()
    district = db.session.query(District).first()

    print(ada.is_within(point_in_both))
    print(district.is_within(point_in_both))
    print()

    print(ada.is_within(point_district))
    print(district.is_within(point_district))
    print(district.is_within(point_far_away))
    print()

    print(ada.distance(point_in_both))
    print(district.distance(point_in_both))
    print()
    print(ada.distance(point_district))
    print(ada.distance(point_far_away))
    print(district.distance(point_far_away))
    print()
    print(ada.is_within(point_in_both))


def main(argv):
    #test_boundaries()
    test_shp_file()


if __name__ == "__main__":
    main(sys.argv)
