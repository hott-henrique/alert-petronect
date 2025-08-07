import time, logging

from petronect.model.PetronectBidding import Attachment

from serverless.FunctionInvoker import FunctionInvoker
from serverless.KeyValueStorage import KeyValueStorage


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    assert isinstance(event, dict)
    assert "bidding_hash" in event
    assert "attachment" in event

    attachment = Attachment.model_validate_json(event["attachment"])

    logger.info(f"Download attachment from bidding ({event['bidding_hash']}): {attachment.DESCRIPTION}.")

    time.sleep(3)

    storage = KeyValueStorage()

    storage_id = f"{event['bidding_hash']}:{attachment.DESCRIPTION}"

    if not storage.exists(storage_id): # For testing only
        data = attachment.download()

        storage.save(storage_id, data)
    else:
        logger.info("Using cache!")

    logger.info(f"Finished downloading attachment from bidding ({event['bidding_hash']}): {attachment.DESCRIPTION}.")

    invoker = FunctionInvoker()

    invoker.trigger(
        "process_bidding_attachment",
        dict(storage_id=storage_id)
    )
