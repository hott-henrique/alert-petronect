import logging

from petronect.model.PetronectBidding import PetronectBidding

from petronect.persistence.Persistence import Persistence
from petronect.persistence.PetronectBiddingPersistence import PetronectBiddingPersistence

from serverless.FunctionInvoker import FunctionInvoker


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    assert isinstance(event, dict)
    assert "bidding" in event

    bidding = PetronectBidding.model_validate(event["bidding"])

    logger.info(f"Processing bidding: {bidding.OPPORT_NUM}.")

    if PetronectBiddingPersistence.exists(event["bidding"]):
        return

    hash = PetronectBiddingPersistence.create(bidding=event["bidding"])

    Persistence.commit()

    for an in bidding.ANEXOS:
        invoker = FunctionInvoker()
        invoker.trigger(
            "download_bidding_attachment",
            dict(bidding_hash=hash, attachment=an.model_dump_json())
        )

    logger.info("Finished processing bidding.")
