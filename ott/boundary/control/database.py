from gtfsdb.model.db import Database as GtfsdbDatabase


class Database(GtfsdbDatabase):

    def __init__(self, **kwargs):
        super(Database, self).__init__(**kwargs)
        self.local_sorted_class_names = [
            'District',
            'Ada'
        ]
        self.sorted_class_names += self.local_sorted_class_names


    @classmethod
    def get_base_subclasses(cls):
        from ott.boundary.model.base import Base
        return Base.__subclasses__()

