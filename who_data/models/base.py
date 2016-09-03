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
    def search(cls, to_dict=True, limit=None, offset=None, **kw):
        q = cls.session.query(cls)

        for k, w in kw.items():
            if w == 'notnull':
                q = q.filter(getattr(cls, k) != None)
            else:
                q = q.filter(getattr(cls, k) == w)

        count = q.count()
        if limit:
            q = q.limit(limit)
        if offset:
            q = q.offset(offset)
        res = q.all()
        if to_dict:
            json_res = []
            for row in res:
                json_res.append(cls.row_to_dict(row))
            return count, json_res
        else:
            return count, res

    @classmethod
    def fetch_first(cls, to_dict=True, **kw):
        q = cls.session.query(cls)
        for k, w in kw.items():
            q = q.filter(getattr(cls, k) == w)
        res = q.first()
        if to_dict and res:
            return cls.row_to_dict(res)
        return res
