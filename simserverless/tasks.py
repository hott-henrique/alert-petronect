from celery import shared_task

import os, sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from serverless.functions.CheckForBiddings import check_for_biddings
from serverless.functions.ProcessNewBidding import process_new_bidding
from serverless.functions.DownloadBiddingAttachment import download_bidding_attachment
from serverless.functions.ProcessBiddingAttachment import process_bidding_attachment
from serverless.functions.MatchBidding import match_bidding
from serverless.functions.SendMatchEmail import send_match_email


@shared_task(name="check_for_biddings")
def check_for_biddings_wrapper(event, context):
    check_for_biddings.lambda_handler(event, context)

@shared_task(name="process_new_bidding")
def process_new_bidding_wrapper(event, context):
    process_new_bidding.lambda_handler(event, context)

@shared_task(name="download_bidding_attachment", rate_limit="45/h")
def download_bidding_attachment_wrapper(event, context):
    download_bidding_attachment.lambda_handler(event, context)

@shared_task(name="process_bidding_attachment")
def process_bidding_attachment_wrapper(event, context):
    process_bidding_attachment.lambda_handler(event, context)

@shared_task(name="match_bidding")
def match_bidding_wrapper(event, context):
    match_bidding.lambda_handler(event, context)

@shared_task(name="send_match_email", rate_limit="35/h")
def send_match_email_wrapper(event, context):
    send_match_email.lambda_handler(event, context)
