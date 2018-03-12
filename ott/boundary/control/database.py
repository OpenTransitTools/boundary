from gtfsdb.model.db import Database as GtfsdbDatabase


class Database(GtfsdbDatabase):

    def __init__(self, **kwargs):
        super(Database, self).__init__(**kwargs)

    @classmethod
    def get_base_subclasses(cls):
        from ott.boundary.model.base import Base
        return Base.__subclasses__()

    @classmethod
    def factory_from_cmdline(cls, args):
        # import pdb; pdb.set_trace()
        kwargs = dict(
            is_geospatial=args.is_geospatial,
            schema=args.schema,
            url=args.database_url,
        )
        db = Database(**kwargs)
        if args.create:
            db.create()
        return db

