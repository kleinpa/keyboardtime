import os
import sys
import appdirs

from software_info import info
from schema import *

data_dir = appdirs.user_data_dir(info['name'], info['author'], info['version'])
if not os.path.exists(data_dir):os.makedirs(data_dir)

db_file = os.path.join(data_dir,"{0}.db3".format(info['exe']))

print("Using database: {0}".format(db_file))

# SQLAlchemy Init
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///{0}'.format(db_file))
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    s = Session()
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()

