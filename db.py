import os
import sys
import appdirs

from schema import *

SOFTWARE_INFO_AUTHOR="Peter Klein"
SOFTWARE_INFO_NAME="METRICS"

data_dir = appdirs.user_data_dir(SOFTWARE_INFO_NAME,SOFTWARE_INFO_AUTHOR,"0.1")
if not os.path.exists(data_dir):os.makedirs(data_dir)

db_file = os.path.join(data_dir,"log-{0}.db3".format(schema_hash))

print("Using database: {0}".format(db_file))


# SQLAlchemy Init
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///{0}'.format(db_file))
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
