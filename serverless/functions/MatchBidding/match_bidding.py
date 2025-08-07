import logging

from petronect.model.PetronectBidding import PetronectBidding
from petronect.persistence.PetronectBiddingPersistence import PetronectBiddingPersistence

from serverless.EmailSender import EmailSender
from serverless.FunctionInvoker import FunctionInvoker
from serverless.KeyValueStorage import KeyValueStorage


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    assert isinstance(event, dict)
    assert "bidding_hash" in event

    bidding_hash = event["bidding_hash"]

    if PetronectBiddingPersistence.is_locked(bidding_hash):
        return

    matches = PetronectBiddingPersistence.get_matches(bidding_hash)

    invoker = FunctionInvoker()

    for m in matches:
        invoker.trigger("send_match_email", m.model_dump())
