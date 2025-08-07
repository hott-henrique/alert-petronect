import typing as t

import sqlalchemy, sqlalchemy.orm

from projectconfig.ProjectConfig import ProjectConfig

from petronect.base.BaseData import BaseData


config = ProjectConfig.instance()

_session: t.Optional[sqlalchemy.orm.Session] = None
_engine: t.Optional[sqlalchemy.Engine] = None

def get_sqlalchemy_session():
    global _engine, _session

    if _engine is None:
        _engine = sqlalchemy.create_engine(str(config.database.url), echo=True)

    if _session is None:
        _session = sqlalchemy.orm.sessionmaker(bind=_engine)()

    return _session
