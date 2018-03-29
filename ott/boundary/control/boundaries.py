from ott.utils import db_utils
from ott.boundary.model.ada import Ada
from ott.boundary.model.district import District

import logging
log = logging.getLogger(__file__)


DEF_BOUNDARY_NAMES=['ada', 'district']


class Boundaries(object):

    db = None
    db_url = None
    db_schema = None

    def __init__(self, db_url, db_schema, boundary_names=DEF_BOUNDARY_NAMES):
        self.db_url = db_url
        self.db_schema = db_schema
        self.boundary_names = boundary_names

    def get_db(self):
        if self.db is None: # or self.db is not connected???
            self.db = db_utils.gtfsdb_conn_parts(self.db_url, self.db_schema, is_geospatial=True)
        return self.db

    def get_boundaries(self):
        # TODO ... improve ... allow new model classes to be added/named/etc with out having to edit this
        if self.db is None:
            self.district = self.ada = None
            db = self.get_db()
            try:
                if self.ada is None:  # or ADA.connection_fails():
                    self.ada = db.session.query(Ada).first()
                if self.district is None:
                    self.district = db.session.query(District).first()
            except Exception as e:
                log.warn(e)

        ret_val = {}
        ret_val['ada'] = self.ada
        ret_val['district'] = self.district
        return ret_val

    def get_within_values(self, point, boundary_names=DEF_BOUNDARY_NAMES):
        ret_val = {}
        b = self.get_boundaries()

        for n in boundary_names:
            boundary = b.get(n)
            if boundary:
                v = boundary.is_within(point)
                ret_val[n] = v
            else:
                ret_val[n] = None
        return ret_val

    def get_distance_values(self, point, boundary_names=DEF_BOUNDARY_NAMES):
        ret_val = {}
        b = self.get_boundaries()

        for n in boundary_names:
            boundary = b.get(n)
            if boundary:
                v = boundary.distance(point)
                ret_val[n] = v
            else:
                ret_val[n] = None
        return ret_val
