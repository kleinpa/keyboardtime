import os
import hashlib

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Numeric

schema_hash = hashlib.md5(open(os.path.abspath(__file__), 'r').read()).hexdigest()
Base = declarative_base()

class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    program = Column(String)
    hostname = Column(String)
    activeness = Column(Numeric)
    duration = Column(Integer)

    def __repr__(self):
        return "<Action(start='%s', program='%s', duration='%s')>" % (
            self.start, self.program, self.duration)
