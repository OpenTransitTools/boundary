from pyramid.response import Response
from pyramid.view import view_config

from ott.utils.parse.url.geo_param_parser import SimpleGeoParamParser
from ott.utils.dao import base

from ott.boundary.control.boundaries import Boundaries

import logging
log = logging.getLogger(__file__)


cache_long = 500
system_err_msg = base.ServerError()


def do_view_config(cfg):
    make_boundaries_global(cfg)
    cfg.add_route('is_within', '/is_within')
    cfg.add_route('is_within_txt', '/is_within_txt')
    cfg.add_route('distance', '/distance')
    cfg.add_route('distance_txt', '/distance_txt')


BOUNDARIES = None
def make_boundaries_global(cfg):
    #import pdb; pdb.set_trace()
    global BOUNDARIES
    db_url = cfg.registry.settings.get('db_url')
    schema = cfg.registry.settings.get('schema')
    BOUNDARIES = Boundaries(db_url, schema)
    return BOUNDARIES


@view_config(route_name='is_within', renderer='json', http_cache=cache_long)
def is_within(request):
    params = SimpleGeoParamParser(request)
    point = params.to_point()
    w = BOUNDARIES.get_within_values(point)
    return w


@view_config(route_name='is_within_txt', renderer='string', http_cache=cache_long)
def is_within_txt(request):
    res = "null response"

    params = SimpleGeoParamParser(request)
    if not params.has_coords():
        res = "don't have coordinates (lat,lon or x,y) specified"
    else:
        point = params.to_point()
        w = BOUNDARIES.get_within_values(point)
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
    d = BOUNDARIES.get_distance_values(point)
    return d


@view_config(route_name='distance_txt', renderer='string', http_cache=cache_long)
def distance_txt(request):
    res = "null response"

    params = SimpleGeoParamParser(request)
    if not params.has_coords():
        res = "don't have coordinates (lat,lon or x,y) specified"
    else:
        point = params.to_point()
        w = BOUNDARIES.get_distance_values(point)
        res = "{} is:\n\n {}' away from the ADA boundary.\n -and-\n {}' away from the DISTRICT boundary.".format(
              point, w['ada'], w['district'])

    return res
