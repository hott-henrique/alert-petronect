import json

import sqlalchemy, sqlalchemy.exc

from petronect.data.UserData import AlertData


from petronect.persistence.session import get_sqlalchemy_session


# from proj.exception.ObjectNotFoundException import ObjectNotFoundException
# from proj.exception.ObjectDuplicatedException import ObjectDuplicatedException



class AlertPersistence(object):

    @classmethod
    def create(cls, alert: AlertData) -> AlertData:
        with get_sqlalchemy_session() as session:
            try:
                session.add(alert)
                session.flush()
                return alert
            except sqlalchemy.exc.IntegrityError as e:
                session.rollback()
                raise Exception(f"Erro ao criar alert: {e}") from e

    @classmethod
    def get(cls, id: int) -> AlertData | None:
        with get_sqlalchemy_session() as session:
            return session.execute(
                sqlalchemy.select(AlertData).where(AlertData.id == id)
            ).scalar_one_or_none()

    @classmethod
    def delete(cls, id: int) -> bool:
        with get_sqlalchemy_session() as session:
            result = session.execute(
                sqlalchemy.delete(AlertData).where(AlertData.id == id)
            )

            return result.rowcount > 0
