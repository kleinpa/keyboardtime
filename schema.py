import os
import hashlib

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Numeric

Base = declarative_base()

class ForegroundApplication(Base):
    __tablename__ = 'foreground_applications'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    application = Column(String)
    hostname = Column(String)
    activeness = Column(Numeric)
    duration = Column(Integer)

    def __repr__(self):
        return "<Application(start='%s', application='%s', duration='%s')>" % (
            self.start, self.application, self.duration)
