import random
import string
import time
import logging
import json
from db_connector import load_words
from fastapi import FastAPI, Request, status
from processor import process_part_of_speech
from models import Words

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

@app.get("/analyze/words", status_code=status.HTTP_200_OK)
async def analyze_words_async():
    logger.info("Test logger")
    words = await load_words()
    logger.info(', '.join([str(elem) for elem in words]))
    return words

@app.get("/analyze/test", status_code=status.HTTP_200_OK)
async def analyze_test_async():
    logger.info("Test logger")
    words = await load_words()
    logger.info(' '.join([str(elem) for elem in words]))
    return words

@app.post("/analyze/speeches", status_code=status.HTTP_201_CREATED)
async def analyze_part_of_speech_async(words: Words):
    logger.info("preparing to analyze given words")
    if len(words.wordList) <= 0:
        return status.HTTP_204_NO_CONTENT
    
    processed_list = process_part_of_speech(words.wordList)
    if len(processed_list) <= 0:
        return status.HTTP_204_NO_CONTENT
    
    return processed_list
