from ott.utils.parse.cmdline import db_cmdline
from ott.boundary.control.database import Database

import logging
log = logging.getLogger(__file__)


def load_db():
    """
    Load GTFS into database
    """
    # import pdb; pdb.set_trace()
    cmdline = db_cmdline.db_parser()
    args = cmdline.parse_args()
    kwargs = vars(args)
    db = Database.factory(**kwargs)
    db.load_tables(**kwargs)
    db.postprocess_tables(**kwargs)


def main():
    load_db()


if __name__ == '__main__':
    main()

