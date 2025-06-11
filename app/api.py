import json
import logging
import requests
import sys
import uuid

from datetime import datetime, timezone
from fastapi import FastAPI, Response, status

from .config import load_config

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("API:      %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


@app.post("/", response_model=str, status_code=status.HTTP_201_CREATED)
def request_work(work_request: dict):
    """Creates a new work request for a given url."""
    config = load_config()

    # get the broker url from the config
    url = config.get("broker", "url")
    if not url:
        raise RuntimeError("Missing broker url in the config file.")
    logger.info("Sending request to the broker at %s.", url)

    # log the work request
    logger.info(f"Work request: {work_request}")

    # create the CloudEvent request headers
    headers = {
        "ce-specversion": "1.0",
        "ce-id": str(uuid.uuid4()),
        "ce-source": "api/request_work",
        "ce-type": "com.api.request_work",
        "ce-time": datetime.now(timezone.utc).isoformat(),
    }

    # create the request data
    data = json.dumps(work_request).encode()

    # send the request to the worker
    r = requests.post(url, headers=headers, data=data, timeout=5)

    logger.info("Work request sent to the worker returned %s.", r.status_code)

    # on any status different from 2xx, raise an exception on the status
    if not r.ok:
        r.raise_for_status()

    # return a status code
    return Response(status_code=status.HTTP_202_ACCEPTED)
