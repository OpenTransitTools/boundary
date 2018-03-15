from pyramid.response import Response
from pyramid.view import view_config

from ott.utils.parse.url.geo_param_parser import SimpleGeoParamParser
from ott.utils.dao import base
from ott.utils import json_utils
from ott.utils import object_utils
from ott.utils import db_utils
from ott.utils import geo_utils

from ott.boundary.model.ada import Ada
from ott.boundary.model.district import District

from .app import CONFIG

import logging
log = logging.getLogger(__file__)


cache_long = 500
system_err_msg = base.ServerError()


db_url = CONFIG.get('db_url')
schema = CONFIG.get('schema')
DB = db_utils.gtfsdb_conn_parts(db_url, schema, is_geospatial=True)


def do_view_config(cfg):
    cfg.add_route('is_within', '/is_within')
    cfg.add_route('is_within_txt', '/is_within_txt')
    cfg.add_route('multi_points_within', '/multi_points_within')


@view_config(route_name='is_within_txt', renderer='string', http_cache=cache_long)
def is_within_txt(request):
    res = "null response"

    params = SimpleGeoParamParser(request)
    if not params.has_coords():
        res = "don't have coordinates (lat,lon or x,y) specified"
    else:
        point = params.to_point()
        ada = DB.session.query(Ada).first()
        district = DB.session.query(District).first()
        a = ada.distance(point)
        d = district.distance(point)
        res = "ada = {}\ndistrict = {}".format(a, d)

    return res


@view_config(route_name='is_within', renderer='json', http_cache=cache_long)
def is_within(request):
    return CONFIG.get('is_within')


@view_config(route_name='multi_points_within', renderer='json', http_cache=cache_long)
def multi_points_within(request):
    url = CONFIG.get('x')
    return url


