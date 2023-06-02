import random
import string
import time
from fastapi import FastAPI, Request
import logging
from db_connector import load_words


logging.config.fileConfig("config/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("ftcore")


app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formated_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formated_process_time}ms status_code={response.status_code}")

    return response

@app.get("/")
def home():
    logger.info("Test logger")
    words = load_words()
    for word in words:
        logger.info(word)
    return words

@app.get("/analyze")
def analyze():
    return None

@app.get("analyze-test")
def analyze_test():
    return None

@app.get("analyze-raw")
def analyze_raw():
    return None

@app.get("authenticate")
def authenticate():
    return None
