from ott.utils.parse.cmdline import db_cmdline
from ott.boundary.control.database import Database

import logging
log = logging.getLogger(__file__)


def load(self, db, **kwargs):
    """
    Load GTFS into database
    """
    # import pdb; pdb.set_trace()

    start_time = time.time()
    log.debug('GTFS.load: {0}'.format(self.file))

    # load known GTFS files, derived tables & lookup tables
    gtfs_directory = self.unzip()
    load_kwargs = dict(
        batch_size=kwargs.get('batch_size', config.DEFAULT_BATCH_SIZE),
        gtfs_directory=gtfs_directory,
    )
    for cls in db.sorted_classes:
        cls.load(db, **load_kwargs)
    shutil.rmtree(gtfs_directory)

    # load route geometries derived from shapes.txt
    if Route in db.classes:
        Route.load_geoms(db)

    # call post process routines...
    do_postprocess = kwargs.get('do_postprocess', True)
    if do_postprocess:
        for cls in db.sorted_classes:
            cls.post_process(db, **kwargs)

    process_time = time.time() - start_time
    log.debug('GTFS.load ({0:.0f} seconds)'.format(process_time))


def load_db():
    cmdline = db_cmdline.db_parser()
    args = cmdline.parse_args()
    kwargs = vars(args)
    db = Database.factory(**kwargs)
    db.load_tables()


def main():
    load_db()


if __name__ == '__main__':
    main()

