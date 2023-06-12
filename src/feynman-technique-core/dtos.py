from dataclasses import dataclass

class Token:
    __slots__ = ["internal_id", "text", "lemma", "upos", "head", "deprel", "feats", "status", "complex", "root", "child"]
    
    def __init__(self, internal_id, text, lemma, upos, head, deprel, feats=None, status=False, complex=False):
        self.internal_id = internal_id # phrase identifier in request
        self.text = text
        self.lemma = lemma
        self.upos = upos #part of speech
        self.head = head #pointer to the root element according to dependency parsing mech, if head == 0 then element is root
        self.deprel = deprel #dependency parsing tag
        self.feats = feats
        self.status = status # informs about presence in database
        self.root = None #head node used to build complex questions
        self.child = [] #child of head used to build complex questions
        self.complex = complex
        
    def __str__(self):
        return f"{self.internal_id}, {self.text}, {self.lemma}, {self.upos}, {self.head}, {self.deprel}, {self.status}, {self.feats}, {self.complex}, {self.root}"   

@dataclass
class WordPresentationResponse:
    id: int
    word: str
    part_of_speech: int
    part_of_speech_name: str
    created_date: str
    context: str
    link: str
