import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import func
from sqlalchemy.orm import class_mapper


class Base(object):
    """

    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, server_default=func.now())
    modified_date = Column(DateTime, onupdate=func.now())

    def for_json(self):
        return self.encode()

    def encode(self, ignore_columns=None):
        if ignore_columns is None:
            ignore_columns = []
        columns = list(set([c.key for c in class_mapper(self.__class__).columns]) - set(ignore_columns))
        return dict((c, self._encode(getattr(self, c))) for c in columns)

    def _encode(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, BaseModel):
            return obj.encode()
        elif isinstance(obj, list):
            return list(map(lambda x: self._encode(x), obj))
        else:
            return obj


BaseModel = declarative_base(cls=Base)
