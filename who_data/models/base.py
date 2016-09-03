from sqlalchemy import create_engine
import configparser
from .meta import Base, DBSession


def set_engine(ini, Base, DBSession):
    config_ini = configparser.ConfigParser()
    config_ini.read(ini)
    engine = create_engine(config_ini['app:main']['sqlalchemy.url'])
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine


class DatastoreBase(Base):
    __abstract__ = True
    __table_args__ = {
        'schema': 'datastore',
    }
    session = DBSession
