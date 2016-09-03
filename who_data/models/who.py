from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import DatastoreBase


class Country(DatastoreBase):
    __tablename__ = 'country'
    id = Column(Text, primary_key=True)  # this should be a 2 char country code
    display_name = Column(Text)


class WHODisease(DatastoreBase):
    __tablename__ = 'disease'
    id = Column(Text, primary_key=True)
    display_name = Column(Text)


class WHODiseaseReport(DatastoreBase):
    __tablename__ = 'disease_report'
    disease_id = Column(Text, primary_key=True)
    country_id = Column(Text, primary_key=True)
    year = Column(Integer, primary_key=True)
    count = Column(Integer)

Index('uq_who_disease_display_name', WHODisease.display_name, unique=True)
Index('ix_who_disease_report_count', WHODiseaseReport.count)
