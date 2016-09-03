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

    @classmethod
    def row_to_dict(cls, row):
        row_dict = {}
        for c in row.__table__._columns:
            row_dict[c.name] = getattr(row, c.name)
        return row_dict

    @classmethod
    def search(cls, to_dict=True, **kw):
        q = cls.session.query(cls)
        count = q.count()
        res = q.all()
        if to_dict:
            json_res = []
            for row in res:
                json_res.append(cls.row_to_dict(row))
            return count, json_res
        else:
            return count, res
