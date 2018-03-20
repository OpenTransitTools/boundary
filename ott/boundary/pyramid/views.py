from pyramid.response import Response
from pyramid.view import view_config

from ott.utils.parse.url.geo_param_parser import SimpleGeoParamParser
from ott.utils.dao import base
from ott.utils import json_utils
from ott.utils import object_utils
from ott.utils.object_utils import SimpleObject
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
    cfg.add_route('distance_txt', '/distance_txt')
    cfg.add_route('multi_points_within', '/multi_points_within')


ADA = None
DISTRICT = None
def get_boundaries():
    try:
        global ADA
        global DISTRICT

        if ADA is None:  # or ADA.connection_fails():
            ADA = DB.session.query(Ada).first()
        if DISTRICT is None:
            DISTRICT = DB.session.query(District).first()
    except Exception as e:
        log.warn(e)

    ret_val = {}
    ret_val['ada'] = ADA
    ret_val['district'] = DISTRICT
    return ret_val


def get_within(point, boundary_names=['ada', 'district']):
    import pdb; pdb.set_trace()

    ret_val = {}
    b = get_boundaries()

    for n in boundary_names:
        boundary = b.get(n)
        if boundary:
            v = boundary.is_within(point)
            ret_val[n] = v
        else:
            ret_val[n] = None
    return ret_val


@view_config(route_name='is_within_txt', renderer='string', http_cache=cache_long)
def is_within_txt(request):
    res = "null response"

    params = SimpleGeoParamParser(request)
    if not params.has_coords():
        res = "don't have coordinates (lat,lon or x,y) specified"
    else:
        point = params.to_point()
        w = get_within(point)
        res = "{}:\n\n {} within the ADA boundary.\n -and-\n {} within the DISTRICT boundary.".format(
              point,
              "is" if w['ada'] else "isn't",
              "is" if w['district'] else "isn't"
        )

    return res


@view_config(route_name='distance_txt', renderer='string', http_cache=cache_long)
def distance_txt(request):
    res = "null response"

    params = SimpleGeoParamParser(request)
    if not params.has_coords():
        res = "don't have coordinates (lat,lon or x,y) specified"
    else:
        point = params.to_point()
        b = get_boundaries()
        if b.ada and b.district:
            a = b.ada.distance(point)
            d = b.district.distance(point)
            res = "{} is:\n\n {}' away from the ADA boundary.\n -and-\n {}' away from the DISTRICT boundary.".format(point, a, d)

    return res


@view_config(route_name='is_within', renderer='json', http_cache=cache_long)
def is_within(request):
    return CONFIG.get('is_within')


@view_config(route_name='multi_points_within', renderer='json', http_cache=cache_long)
def multi_points_within(request):
    url = CONFIG.get('x')
    return url

