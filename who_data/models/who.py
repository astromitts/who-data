from sqlalchemy import (
    Column,
    Integer,
    Text,
)
from sqlalchemy.dialects import postgresql
from .base import DatastoreBase


class Country(DatastoreBase):
    __tablename__ = 'country'
    id = Column(Text, primary_key=True)  # this should be a 2 char country code
    name = Column(Text)
    alias = Column(postgresql.ARRAY(Text))
    url_name = Column(Text)

    @classmethod
    def upsert(cls, id, name, url_name, alias):
        '''
        update object by id if it exists, otherwise create it
        '''
        if not alias:
            alias = []
        q = cls.session.query(cls).filter(cls.id == id)
        existing = q.first()
        if existing:
            existing.name = name
            existing.url_name = url_name
            if alias:
                for a in alias:
                    if a.lower() not in existing.alias:
                        existing.alias.append(a.lower())
            cls.session.flush()
            return existing
        new_cls = cls(
            id=id,
            name=name,
            url_name=url_name,
            alias=[a.lower() for a in alias]
        )
        cls.session.add(new_cls)
        cls.session.flush()
        return new_cls


class WHODisease(DatastoreBase):
    __tablename__ = 'disease'
    id = Column(Text, primary_key=True)
    name = Column(Text)

    @classmethod
    def upsert(cls, id, name):
        q = cls.session.query(cls).filter(cls.id == id)
        existing = q.first()
        if existing:
            existing.name = name
            cls.session.flush()
            return existing
        new_cls = cls(
            id=id,
            name=name,
        )
        cls.session.add(new_cls)
        cls.session.flush()
        return new_cls


class WHODiseaseReport(DatastoreBase):
    __tablename__ = 'disease_report'
    disease_id = Column(Text, primary_key=True)
    country_id = Column(Text, primary_key=True)
    year = Column(Integer, primary_key=True)
    report_count = Column(Integer)

    @classmethod
    def upsert(cls, disease_id, country_id, year, report_count):
        q = cls.session.query(cls)
        q = q.filter(cls.disease_id == disease_id)
        q = q.filter(cls.country_id == country_id)
        q = q.filter(cls.year == year)
        existing = q.first()
        if existing:
            existing.report_count = report_count
            cls.session.flush()
            return existing

        new_cls = cls(
            country_id=country_id,
            disease_id=disease_id,
            year=year,
            report_count=report_count
        )
        cls.session.add(new_cls)
        cls.session.flush()
        return new_cls
