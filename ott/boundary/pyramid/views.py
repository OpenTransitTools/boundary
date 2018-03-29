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


import logging
log = logging.getLogger(__file__)


cache_long = 500
system_err_msg = base.ServerError()


DB = None


def do_view_config(cfg):
    #import pdb; pdb.set_trace()
    global DB
    db_url = cfg.registry.settings.get('db_url')
    schema = cfg.registry.settings.get('schema')
    DB = db_utils.gtfsdb_conn_parts(db_url, schema, is_geospatial=True)

    cfg.add_route('is_within', '/is_within')
    cfg.add_route('is_within_txt', '/is_within_txt')
    cfg.add_route('distance', '/distance')
    cfg.add_route('distance_txt', '/distance_txt')


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


def get_within_values(point, boundary_names=['ada', 'district']):
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


def get_distance_values(point, boundary_names=['ada', 'district']):
    ret_val = {}
    b = get_boundaries()

    for n in boundary_names:
        boundary = b.get(n)
        if boundary:
            v = boundary.distance(point)
            ret_val[n] = v
        else:
            ret_val[n] = None
    return ret_val


@view_config(route_name='is_within', renderer='json', http_cache=cache_long)
def is_within(request):
    params = SimpleGeoParamParser(request)
    point = params.to_point()
    w = get_within_values(point)
    return w


@view_config(route_name='is_within_txt', renderer='string', http_cache=cache_long)
def is_within_txt(request):
    res = "null response"

    params = SimpleGeoParamParser(request)
    if not params.has_coords():
        res = "don't have coordinates (lat,lon or x,y) specified"
    else:
        point = params.to_point()
        w = get_within_values(point)
        res = "{}:\n\n {} within the ADA boundary.\n -and-\n {} within the DISTRICT boundary.".format(
              point,
              "is" if w['ada'] else "isn't",
              "is" if w['district'] else "isn't"
        )

    return res


@view_config(route_name='distance', renderer='json', http_cache=cache_long)
def distance(request):
    params = SimpleGeoParamParser(request)
    point = params.to_point()
    d = get_distance_values(point)
    return d


@view_config(route_name='distance_txt', renderer='string', http_cache=cache_long)
def distance_txt(request):
    res = "null response"

    params = SimpleGeoParamParser(request)
    if not params.has_coords():
        res = "don't have coordinates (lat,lon or x,y) specified"
    else:
        point = params.to_point()
        w = get_distance_values(point)
        res = "{} is:\n\n {}' away from the ADA boundary.\n -and-\n {}' away from the DISTRICT boundary.".format(
              point, w['ada'], w['district'])

    return res
