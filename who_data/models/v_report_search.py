from sqlalchemy import (
    Column,
    Integer,
    Text,
)
from sqlalchemy import func
from .base import DatastoreBase


class ReportSearch(DatastoreBase):
    __tablename__ = 'v_reports_search'
    disease_id = Column(Text, primary_key=True)
    country_id = Column(Text, primary_key=True)
    year = Column(Integer, primary_key=True)
    count = Column(Integer)
    country_name = Column(Text)
    country_url_name = Column(Text)
    disease_name = Column(Text)

    @classmethod
    def order_search(cls, q):
        q = q.order_by(cls.country_name)
        q = q.order_by(cls.year)
        q = q.order_by(cls.count)
        return q

    @classmethod
    def filter_country(cls, q, phrase):
        if len(phrase) == 2:
            q = q.filter(cls.country_id == phrase.upper())
        else:
            q = q.filter(func.lower(cls.country_name) == phrase.lower())
        return q
