from petronect.persistence.session import get_sqlalchemy_session


class Persistence(object):

    @classmethod
    def commit(cls):
        session = get_sqlalchemy_session()

        session.commit()

    @classmethod
    def rollback(cls):
        session = get_sqlalchemy_session()

        session.rollback()

    @classmethod
    def finish(cls):
        session = get_sqlalchemy_session()

        session.close_all()
