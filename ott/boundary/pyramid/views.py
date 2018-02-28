from pyramid.response import Response
from pyramid.view import view_config

from ott.utils.parse import GeoParamParser

from ott.utils.dao import base
from ott.utils import json_utils
from ott.utils import object_utils

from .app import CONFIG

import logging
log = logging.getLogger(__file__)


cache_long = 500
system_err_msg = base.ServerError()


def do_view_config(cfg):
    cfg.add_route('is_within', '/is_within')
    cfg.add_route('is_within_txt', '/is_within_txt')
    cfg.add_route('multi_points_within', '/multi_points_within')


@view_config(route_name='is_within_txt', renderer='string', http_cache=cache_long)
def is_within_txt(request):
    query = session.query(Lake).filter(Lake.geom.ST_Contains('POINT(4 1)'))
    for lake in query:
        print lake.name

    return CONFIG.get('db_layers')


@view_config(route_name='is_within', renderer='json', http_cache=cache_long)
def is_within(request):
    #GeoParamParser
    return CONFIG.get('is_within')


@view_config(route_name='multi_points_within', renderer='json', http_cache=cache_long)
def multi_points_within(request):
    url = CONFIG.get('x')
    return url


