from ott.utils.parse.cmdline import db_cmdline
from ott.boundary.control.database import Database

import logging
log = logging.getLogger(__file__)


def load_db():
    cmdline = db_cmdline.db_parser()
    args = cmdline.parse_args()
    db = Database.factory_from_cmdline(args)



def XXload_db():
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

