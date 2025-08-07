from nltk import data
import sqlalchemy, sqlalchemy.exc

from petronect.data.PetronectAttachmentData import PetronectAttachmentData
from petronect.persistence.session import get_sqlalchemy_session

from petronect.model.PetronectBidding import Attachment, PetronectBidding

from petronect.data.PetronectBiddingData import PetronectBiddingData

# from proj.exception.ObjectNotFoundException import ObjectNotFoundException
# from proj.exception.ObjectDuplicatedException import ObjectDuplicatedException


class PetronectAttachmentPersistence(object):

    @classmethod
    def create(cls, bidding_hash: str, name: str, tokens: set[str]):
        session = get_sqlalchemy_session()

        session.add(PetronectAttachmentData(
            bidding_hash=bidding_hash,
            file=name,
            tokens=tokens
        ))

        session.flush()
