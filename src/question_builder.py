from models import QuestionResponse
from dtos import Token
from models import AnalyzeSentenceRequest
from constants import (
    PartOfSpeechEnum, 
    NumberFeatureValueConst, 
    AnimacyFeatureValueConst, 
    GenderFeatureValueConst, 
    UniversalFeaturesConst, 
    part_of_speech_mapper
)

def create_questions(
        responses: list[QuestionResponse], 
        analyze_request: AnalyzeSentenceRequest, 
        dtokens: list[Token], 
        words: list[str]) -> list[QuestionResponse]:
    
    for token in dtokens:
        token.status = set_status(token, words)
        log_presence(token.status, token.lemma)
        if(token.status == False 
        and token.upos != PartOfSpeechEnum.INNE 
        and token.upos != PartOfSpeechEnum.PUNKT 
        and token.upos != PartOfSpeechEnum.SPÓJNIK_KOORDYNACYJNY 
        and token.upos != PartOfSpeechEnum.WYKRZYKNIK
        and token.upos != PartOfSpeechEnum.ZAIMEK
        and token.upos != PartOfSpeechEnum.ZAIMEK_WSKAZUJĄCY
        and token.upos != PartOfSpeechEnum.SPÓJNIK
        and token.upos != PartOfSpeechEnum.SYMBOL
        and token.upos != PartOfSpeechEnum.PARTYKUŁA
        and token.upos != PartOfSpeechEnum.PRZYSŁÓWEK):
            response = QuestionResponse(
                        id = analyze_request.id,
                        level = analyze_request.level + 1,
                        sentence = analyze_request.sentence,
                        parent_id = analyze_request.id,
                        question = question_builder(token),
                        word_length = len(analyze_request.sentence),
                        children = [])
                        
            if response.question == None:
                continue
            responses.append(response)
            
def create_questions_text(
        responses: list[QuestionResponse], 
        dtokens: list[Token], 
        words: list[str]) -> list[QuestionResponse]:
     
     for token in dtokens:
        token.status = set_status(token, words)
        log_presence(token.status, token.lemma)
        if(token.status == False 
        and token.upos != PartOfSpeechEnum.INNE 
        and token.upos != PartOfSpeechEnum.PUNKT 
        and token.upos != PartOfSpeechEnum.SPÓJNIK_KOORDYNACYJNY 
        and token.upos != PartOfSpeechEnum.WYKRZYKNIK
        and token.upos != PartOfSpeechEnum.ZAIMEK
        and token.upos != PartOfSpeechEnum.ZAIMEK_WSKAZUJĄCY
        and token.upos != PartOfSpeechEnum.SPÓJNIK
        and token.upos != PartOfSpeechEnum.SYMBOL
        and token.upos != PartOfSpeechEnum.PARTYKUŁA
        and token.upos != PartOfSpeechEnum.PRZYSŁÓWEK):
            question = question_builder(token)
            if question == None:
                continue
            responses.append(question)


def set_status(token: Token, words: list[str]) -> bool:
    if token.lemma in words and token.status == False:
        return True
    elif token.status == True:
        return True
    else:
        return False
    
def log_presence(status: bool, word: str) -> str:
    if status == None or word == None:
        return
    
    if status == False:
        return f"{word} NOT exists in database"
    elif status == True:
        return f"{word} exists in database"
    else:
        return f"{word} NOT exists in database"


def question_builder(phrase: Token) -> str:
    match phrase.complex:
        case True:
            return build_complex(phrase)
        case False:
            return build(phrase)
        case _:
            return None

def build(token: Token) -> str:
    pos = part_of_speech_mapper(token.upos)
    match pos:
        case PartOfSpeechEnum.CZASOWNIK.value:
            return verb_builder(token.lemma)
        case PartOfSpeechEnum.RZECZOWNIK.value:
            animacy = token.feats.get(UniversalFeaturesConst.Animacy) if hasattr(token, "feats") or token.feats == None else None
            return noun_builder(token.lemma, animacy)
        case PartOfSpeechEnum.PRZYMIOTNIK.value:
            number = token.feats.get(UniversalFeaturesConst.Number) if hasattr(token, "feats") or token.feats == None else None
            return adj_builder(token.text, number)
        case PartOfSpeechEnum.RZECZOWNIK_ODPOWIEDNI.value:
            return propn_builder(token.lemma)
        case _:
            return None

def build_complex(token: Token) -> str:
    if token.root != None:
        return build_with_head_reference(token)
    elif token.child != None:
        return build_with_children_reference(token)
    else:
        return None

def build_with_head_reference(token: Token) -> str:
    pos = part_of_speech_mapper(token.upos)
    root_pos = ""
    if token.root != None:
        root_pos = part_of_speech_mapper(token.root.upos)

    #TODO: Do zbadania!
    if pos == PartOfSpeechEnum.PRZYMIOTNIK.value and (root_pos == PartOfSpeechEnum.RZECZOWNIK.value or root_pos == PartOfSpeechEnum.CZASOWNIK.value):
        gender = token.root.feats.get(UniversalFeaturesConst.Gender) if hasattr(token.root, "feats") or token.root.feats == None else None
        return build_head_reference_adj(token.root.lemma, token.lemma, gender)
    else:
        return None

def build_with_children_reference(token: Token) -> str:
    pos = part_of_speech_mapper(token.upos)
    child = token.child[0]
    match pos:
        case PartOfSpeechEnum.RZECZOWNIK.value:
            if child.upos == PartOfSpeechEnum.RZECZOWNIK:                
                gender = token.feats.get(UniversalFeaturesConst.Gender) if hasattr(token, "feats") or token.feats == None else None
                return build_children_reference(token.lemma,
                                                token.child,
                                                gender)
            else: 
                return build(token)
        case _:
            return None
        
@staticmethod
def adj_builder(phrase: str, number: str) -> str:
    if number == NumberFeatureValueConst.PluralNumber:
         return f"Dlaczego {number_switcher(number)} {phrase_adj_switcher(phrase)}?"
    return f"Dlaczego {number_switcher(number)} {phrase}?"

@staticmethod
def noun_builder(phrase: str, animacy: str):
    return f"{animacy_switcher(animacy)} jest {phrase}?"

@staticmethod
def verb_builder(phrase: str) -> str:
    return f"Co robi {phrase}?"

@staticmethod
def propn_builder(phrase: str) -> str:
    return f"Co to znaczy {phrase}?"

@staticmethod
def build_head_reference_adj(head: str, child: str, gender: str) -> str:
    children_text = ''.join(gender_switcher(child, gender))
    return f"Dlaczego {head} jest {children_text}?"

@staticmethod 
def build_children_reference(head: str, children: Token, gender: str) -> str:
    children_text = ''.join(get_lemma_from_child(children))
    children_lemma = gender_switcher(children_text, gender)
    head = head + " " + children_lemma
    return f"Co to znaczy {head}?"

@staticmethod
def fem_builder(phrase: str) -> str:
    changed_phrase = "a".join(phrase.rsplit(phrase[-1:], 1))
    return changed_phrase
    
@staticmethod
def neut_builder(phrase: str) -> str:
    changed_phrase = "e".join(phrase.rsplit(phrase[-1:], 1))
    return changed_phrase

@staticmethod
def com_builder(phrase: str) -> str:
    changed_phrase = "x".join(phrase.rsplit(phrase[-1:], 1))
    return changed_phrase

@staticmethod
def get_lemma_from_child(children: Token) -> str:
    if len(children) <= 0:
        return
    child = children[0]
    return child.lemma

@staticmethod
def gender_switcher(phrase: str, gender: str) -> str:
    if phrase == None:
        return ""
    
    match gender:
        case GenderFeatureValueConst.Masculine:
            return phrase
        case GenderFeatureValueConst.Feminine:
            return fem_builder(phrase)
        case GenderFeatureValueConst.Neuter:
            return neut_builder(phrase)
        case GenderFeatureValueConst.Common:
            return com_builder(phrase)
        case _:
            return phrase
        
@staticmethod
def number_switcher(number: str) -> str:
    if number == None:
        return "jest"
    match number:
        case NumberFeatureValueConst.SingularNumber:
            return "jest"
        case NumberFeatureValueConst.PluralNumber:
            return "są"
        case _:
            return "jest"
        
@staticmethod
def phrase_adj_switcher(phrase: str) -> str:
    if phrase == None:
        return phrase
    
    return neut_builder(phrase)
        
@staticmethod
def animacy_switcher(animacy: str) -> str:
    if animacy == None:
        return "Co to"
    
    match animacy:
        case AnimacyFeatureValueConst.Animate:
            return "Co to"
        case AnimacyFeatureValueConst.Inanimate:
            return "Co to"
        case AnimacyFeatureValueConst.Human:
            return "Kto to"
        case AnimacyFeatureValueConst.NonHuman:
            return "Co to"
        case _:
            return "Co to"
          