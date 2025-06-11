import logging
import sys
import time

from fastapi import BackgroundTasks, FastAPI, Response, status


app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("WORKER:   %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


def do_the_work(work_info: dict):
    """Execute the work request."""

    logger.info("Executing work: %s", work_info["work"])

    # simulate the work execution
    time.sleep(work_info["duration"])

    logger.info("Work completed: %s", work_info["work"])


@app.post("/")
def schedule_the_work(work_info: dict, background_tasks: BackgroundTasks):
    """Schedule a new work request."""

    # log the work information
    logger.info(f"Received the following work information: {work_info}")

    # execute the work in background
    background_tasks.add_task(do_the_work, work_info)

    # OpenShift Serverless needs an explicit return, or it retries the request until it fails
    return Response(status_code=status.HTTP_202_ACCEPTED)
