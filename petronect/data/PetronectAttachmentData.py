import typing as t

from sqlalchemy import (String, Text, ForeignKey)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)
from sqlalchemy.dialects.postgresql import ARRAY

from petronect.base.BaseData import BaseData

if t.TYPE_CHECKING:
    from petronect.data.PetronectBiddingData import PetronectBiddingData


class PetronectAttachmentData(BaseData):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bidding_hash: Mapped[str] = mapped_column(ForeignKey("biddings.hash", ondelete="CASCADE"))
    file: Mapped[str] = mapped_column(Text)
    tokens: Mapped[t.List[str]] = mapped_column(ARRAY(String))

    bidding: Mapped["PetronectBiddingData"] = relationship(back_populates="attachments")
