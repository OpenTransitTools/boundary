from ott.utils.parse.cmdline import db_cmdline

import logging
logging.basicConfig()
log = logging.getLogger(__file__)


def make_session(url, schema, is_geospatial=False, create_db=False):
    return Database.make_session(url, schema, is_geospatial, create_db)


def load_data(session, agency_id, trips_url, alerts_url, vehicles_url):
    ret_val = True
    return ret_val


def parse(session, agency_id, feed_url, clear_first=False):
    ret_val = True
    return ret_val


def load_db():
    cmdline = db_cmdline.db_parser()
    args = cmdline.parse_args()
    print args
    exit
    session = Database.make_session(args.database_url, args.schema, args.geo, args.create)

    url = 'http://trimet.org/transweb/ws/V1/FeedSpecAlerts/appId/3819A6A38C72223198B560DF0/includeFuture/true'
    url = 'http://trimet.org/transweb/ws/V1/TripUpdate/appId/3819A6A38C72223198B560DF0/includeFuture/true'
    #url = 'http://developer.trimet.org/ws/gtfs/VehiclePositions/appId/3819A6A38C72223198B560DF0'
    if args.url and len(args.url) > 1:
        url = args.url
    parse(session, args.agency, url, args.clear)


def main():
    load_db()

if __name__ == '__main__':
    main()

