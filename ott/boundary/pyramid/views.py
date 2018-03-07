from pyramid.response import Response
from pyramid.view import view_config

from ott.utils.parse.geo_param_parser import SimpleGeoParamParser
from ott.utils.dao import base
from ott.utils import json_utils
from ott.utils import object_utils
from ott.utils import db_utils
from ott.utils import geo_utils

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
    res = "null response"

    params = SimpleGeoParamParser(request)
    if not params.has_coords():
        res = "don't have coordinates (lat,lon or x,y) specified"
    else:
        res = "hey hey, we have coords"

        #res = CONFIG.get('is_within')
        """
        db = get 
        ada = db.session.query(Ada).first()
        district = db.session.query(District).first()
    
        res = []
        r = ada.intersect(point_district)
        res.append(r)
    
        r = district.intersect(point_district)
        res.append(r)
    
        for r in res:
            pass
        """

    return res


@view_config(route_name='is_within', renderer='json', http_cache=cache_long)
def is_within(request):
    return CONFIG.get('is_within')


@view_config(route_name='multi_points_within', renderer='json', http_cache=cache_long)
def multi_points_within(request):
    url = CONFIG.get('x')
    return url


