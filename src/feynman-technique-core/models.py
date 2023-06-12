from typing import List
from pydantic import BaseModel
from datetime import datetime

class Word(BaseModel):
    id: int
    word: str
    part_of_speech: int
    created_date: datetime
    context: str
    link: str

class PartOfSpeech(BaseModel):
    id: int
    name: str

class User(BaseModel):
    id: int
    role: int
    name: str
    password: str
    created_date: datetime

class Role(BaseModel):
    id: int
    name: str

class Words(BaseModel):
    wordList: list[str]

class DetailedWordRequest(BaseModel):
    source: str
    words: list[str]

class AnalyzeSentenceRequest(BaseModel):
    id: int
    level: int
    sentence: str
    understood_words: list[str]

class QuestionResponse(BaseModel):
    id: int
    level: int
    sentence: str
    parent_id: int
    question: str
    word_length: int
    children: list

class AnalyzeSentenceResponse(BaseModel):
    questions: list[QuestionResponse]
    understood_words: list[str]
    
    class Config:
            validate_assignment = True
        
class DetailedWordKeyResponse(BaseModel):
    name: str
    lemma: str
    part_of_speech: str

class DetailedWordResponse(BaseModel):
    source: str
    words: list[DetailedWordKeyResponse]

