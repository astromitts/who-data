from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .base import DatastoreBase


class Country(DatastoreBase):
    __tablename__ = 'country'
    id = Column(Text, primary_key=True)  # this should be a 2 char country code
    name = Column(Text)

    @classmethod
    def create_get_by_id(cls, id, name):
        '''
        get object by id if it exists, otherwise create it
        '''
        q = cls.session.query(cls).filter(cls.id == id)
        existing = q.first()
        if existing:
            return existing
        new_cls = cls(
            id=id,
            name=name
        )
        cls.session.add(new_cls)
        cls.session.flush()
        return new_cls


class WHODisease(DatastoreBase):
    __tablename__ = 'disease'
    id = Column(Text, primary_key=True)
    name = Column(Text)


class WHODiseaseReport(DatastoreBase):
    __tablename__ = 'disease_report'
    disease_id = Column(Text, primary_key=True)
    country_id = Column(Text, primary_key=True)
    year = Column(Integer, primary_key=True)
    count = Column(Integer)
