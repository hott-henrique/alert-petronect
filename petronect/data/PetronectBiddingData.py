import datetime as dt, typing as t

from sqlalchemy import (Integer, String, JSON)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)

from petronect.base.BaseData import BaseData

if t.TYPE_CHECKING:
    from petronect.data.PetronectAttachmentData import PetronectAttachmentData


class PetronectBiddingData(BaseData):
    __tablename__ = "biddings"

    hash: Mapped[str] = mapped_column(String, primary_key=True)

    data: Mapped[JSON] = mapped_column(JSON)
    locks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="""
            This field help controlling when this bidding has all files processed.
            The function that matches it with alerts can check: bidding.locks == 0.
            Meaning, no file of this bidding is being processed.
        """
    )

    attachments: Mapped[t.List["PetronectAttachmentData"]] = relationship(
        back_populates="bidding", cascade="all, delete-orphan"
    )
