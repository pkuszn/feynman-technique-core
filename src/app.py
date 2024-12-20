import asyncio
import random
import string
import time
import logging
import configparser
from fastapi import FastAPI, Request, status
from processor import process_part_of_speech
from question_builder import create_questions
from communication import get_words_async

from processor import (
    try_process, 
    create_dependencies
)

from utils import (
    auto_correct, 
    correct_tokens, 
    distinct_sentences, 
    remove_response_duplicates
)

from models import (
    TokenResponse, 
    WordRequest, 
    ScraperTokenResponse, 
    AnalyzeSentenceRequest, 
    AnalyzeSentenceResponse
)

logging.config.fileConfig("config/logging.conf", disable_existing_loggers=False)

config = configparser.ConfigParser()
config.read('./config/config.ini')

logger = logging.getLogger("ftcore")

APP_NAME = config['application']['appName']
APP_VER = config['application']['version']
APP_PORT = config['application']['port']
APP_DESC = config['application']['description']

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

@app.get('/info')
async def info(i: str):
    return APP_NAME + ": " + APP_VER + ": " + APP_PORT + ": " + APP_DESC

app.get("/test")
async def test(data: str):
    return {"data": data}

@app.get("/analyze/words", status_code=status.HTTP_200_OK)
async def analyze_words_async() -> list:
    logger.info("Getting words...")
    words = await asyncio.gather(get_words_async())
    logger.info(', '.join([str(elem) for elem in words]))
    return words

@app.post("/analyze/speeches", status_code=status.HTTP_200_OK)
async def analyze_speeches_async(words: list[WordRequest]) -> list[ScraperTokenResponse]:
    logger.info("Preparing to analyze given words")
    if len(words) <= 0:
        return status.HTTP_204_NO_CONTENT
    detailed_words = []
    for chunk in words:
        detailed_word = ScraperTokenResponse(source=chunk.source, words=process_part_of_speech(chunk.words))
        detailed_words.append(detailed_word)
    if len(detailed_word.words) <= 0:
        return status.HTTP_204_NO_CONTENT
    return detailed_words

@app.post('/analyze/speeches/text', status_code=status.HTTP_200_OK)
async def analyze_speeches_raw_async(words: list[str]) -> list[TokenResponse]:
    logger.info('Preparing to analyze given words')
    if words == None or len(words) == 0:
        return status.HTTP_204_NO_CONTENT
    detailed_word_key_list = process_part_of_speech(words)
    if detailed_word_key_list == None or len(detailed_word_key_list) == 0:
        return status.HTTP_400_BAD_REQUEST
    return detailed_word_key_list

@app.post("/analyze", status_code=status.HTTP_200_OK)
async def analyze_sentences(analyze_request: AnalyzeSentenceRequest) -> AnalyzeSentenceResponse:
    try:
        if analyze_request == None:
            return status.HTTP_204_NO_CONTENT
        responses = []
        cls_sentences = auto_correct(analyze_request.sentence)
        if cls_sentences == None or len(cls_sentences) <= 0:
            logger.error("Couldn't processed request. Autocorrection failed")
            return status.HTTP_204_NO_CONTENT
        tokens = try_process(cls_sentences)
        if tokens == None or len(tokens) <= 0:
            logger.error("Couldn't processed request. Lemmatization failed.")
            return status.HTTP_204_NO_CONTENT
        cls_tokens = correct_tokens(tokens)
        if cls_tokens == None or len(cls_tokens) <= 0:
            logger.error("Couldn't processed request. Removing typos failed.")
            return status.HTTP_204_NO_CONTENT
        dtokens = distinct_sentences(cls_tokens, analyze_request.understood_words)
        if dtokens == None or len(dtokens) <= 0:
            logger.error("Couldn't processed request. Distinct operation failed")
            return status.HTTP_204_NO_CONTENT
        prep_tokens = create_dependencies(dtokens)  
        if prep_tokens == None or len(prep_tokens) <= 0:
            logger.error("Couldn't processed request. Creating dependencies failed.")
            return status.HTTP_204_NO_CONTENT
        words = await asyncio.gather(get_words_async())
        lemmas = [x.lemma for x in prep_tokens]
        create_questions(responses, analyze_request, prep_tokens, words)
        dresponses = remove_response_duplicates(responses)
        if dresponses == None or len(dresponses) <= 0:
            logger.error("Couldn't procesed request. Removing duplicates failed.")
            return status.HTTP_204_NO_CONTENT
        response = AnalyzeSentenceResponse(questions = dresponses, understood_words = lemmas)
        return response
    except Exception as e:
        logger.exception(e)
        return status.HTTP_400_BAD_REQUEST