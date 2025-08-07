import hashlib, json

import sqlalchemy, sqlalchemy.exc

from sqlalchemy.sql import text

from petronect.persistence.session import get_sqlalchemy_session

from petronect.base.BaseModel import BaseModel

from petronect.data.PetronectBiddingData import PetronectBiddingData

# from proj.exception.ObjectNotFoundException import ObjectNotFoundException
# from proj.exception.ObjectDuplicatedException import ObjectDuplicatedException


class AlertMatching(BaseModel):
    alert_id: int
    bidding: str
    files: list[str]

class PetronectBiddingPersistence(object):

    @classmethod
    def create(cls, bidding: dict) -> str:
        session = get_sqlalchemy_session()

        try:
            hash = hashlib.md5(json.dumps(bidding, sort_keys=True, default=str).encode("utf-8")).hexdigest()

            session.add(PetronectBiddingData(hash=hash, data=bidding))

            session.flush()
        except sqlalchemy.exc.IntegrityError:
            raise Exception(f"Already exist bidding with number {bidding['OPPORT_NUM']!r}")

        return hash

    @classmethod
    def get(cls, hash: str) -> PetronectBiddingData | None:
        stmt = sqlalchemy.select(PetronectBiddingData).where(
            PetronectBiddingData.hash == hash
        )

        with get_sqlalchemy_session() as session:
            result = session.execute(stmt).scalar_one_or_none()

        return result

    @classmethod
    def exists(cls, bidding: dict) -> bool:
        hash = hashlib.md5(json.dumps(bidding, sort_keys=True).encode("utf-8")).hexdigest()

        stmt = sqlalchemy.select(PetronectBiddingData.hash).where(
            PetronectBiddingData.hash == hash
        )

        with get_sqlalchemy_session() as session:
            result = session.execute(stmt).scalar_one_or_none()

        return result is not None

    @classmethod
    def lock(cls, hash: str) -> bool:
        stmt = (
            sqlalchemy.update(PetronectBiddingData)
                      .where(PetronectBiddingData.hash == hash)
                      .values(running_locks=PetronectBiddingData.locks + 1)
        )

        with get_sqlalchemy_session() as session:
            result = session.execute(stmt)
            session.commit()

        return result.rowcount > 0

    @classmethod
    def unlock(cls, number: str) -> bool:
        with get_sqlalchemy_session() as session:
            current = session.execute(
                sqlalchemy.select(PetronectBiddingData.locks).where(
                    PetronectBiddingData.hash == hash
                )
            ).scalar_one_or_none()

            if current is None or current <= 0:
                return False

            stmt = (
                sqlalchemy.update(PetronectBiddingData)
                          .where(PetronectBiddingData.hash == hash)
                          .values(running_locks=PetronectBiddingData.locks - 1)
            )
            result = session.execute(stmt)
            session.commit()

        return result.rowcount > 0

    @classmethod
    def is_locked(cls, hash: str) -> bool:
        stmt = sqlalchemy.select(PetronectBiddingData.locks).where(
            PetronectBiddingData.hash == hash
        )

        with get_sqlalchemy_session() as session:
            result = session.execute(stmt).scalar_one_or_none()

        return result is not None and result > 0

    @classmethod
    def get_matches(cls, hash: str, min_common_tokens: int = 1) -> list[AlertMatching]:
        sql = text("""
            WITH bidding_tokens AS (
                SELECT
                    bidding_hash,
                    file,
                    unnest(tokens) AS token
                FROM attachments
                WHERE bidding_hash = :bidding_hash
            ),
            tag_matches AS (
                SELECT
                    tags.id AS tag_id,
                    bt.bidding_hash,
                    bt.file AS matched_file,
                    COUNT(*) AS matched_tokens
                FROM tags
                JOIN bidding_tokens bt
                    ON bt.token = ANY(tags.tokens)
                GROUP BY tags.id, bt.bidding_hash, bt.file
            )
            SELECT
                tag_id,
                bidding_hash as bidding,
                ARRAY_AGG(DISTINCT matched_file) AS files
            FROM tag_matches
            GROUP BY tag_id, bidding_hash;
        """)

        with get_sqlalchemy_session() as session:
            result = session.execute(sql, {
                "bidding_hash": hash,
                "min_common_tokens": min_common_tokens
            })

            return [ AlertMatching.model_validate(row) for row in result.mappings() ]
