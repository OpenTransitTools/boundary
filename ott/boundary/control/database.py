from gtfsdb.model.db import Database as GtfsdbDatabase


class Database(GtfsdbDatabase):

    def __init__(self, **kwargs):
        super(Database, self).__init__(**kwargs)
        self.sorted_class_names.append('District')
        self.sorted_class_names.append('Ada')

    @classmethod
    def get_base_subclasses(cls):
        from ott.boundary.model.base import Base
        return Base.__subclasses__()

