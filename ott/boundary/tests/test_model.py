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
        log.warn(e)
        log.warn("couldn't make the BasicModelTests object for some reason")

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


def test_boundaries():
    """
    run by main, will test boundary intersection in established Geo database, with existing populated boundary tables
    """
    from ott.utils import db_utils
    from ott.utils import geo_utils
    point_in_both  = geo_utils.make_point_srid(lat=45.5, lon=-122.5)
    point_district = geo_utils.make_point_srid(lat=45.5, lon=-122.5)
    point_far_away = geo_utils.make_point_srid(lat=45.5, lon=-122.5)


    # bin/python
    db = db_utils.db_args_gtfsdb()
    ada = db.session.query(Ada).first()
    district = db.session.query(District)

    print ada
    print ada.intersect(point_far_away)
    print ada.distance(point_far_away)


def main(argv):
    test_boundaries()


if __name__ == "__main__":
    main(sys.argv)
