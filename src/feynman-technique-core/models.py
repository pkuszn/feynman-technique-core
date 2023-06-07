from typing import Optional
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
    wordList: list
