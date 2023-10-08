from constants import TypoFeatureValueConst, UniversalFeaturesConst
from autocorrect import Speller 
from dtos import Token

#TODO: Nazwy własne traktowane jako literówki!
def auto_correct(sentences: list) -> Speller:
    if len(sentences) <= 0:
        return sentences
    
    spell = Speller('pl')
    return spell(sentences)

def correct_tokens(tokens: list[Token]) -> list[Token]:
    if len(tokens) <= 0:
        return tokens
    
    for token in tokens:
        is_typo = type_checker(token.feats, UniversalFeaturesConst.Typo) if hasattr(token, "feats") else None
        if is_typo != None and is_typo == TypoFeatureValueConst.IsTypo:
            tokens.remove(token)
            
    return tokens
        
def distinct_sentences(tokens: list[Token], understood_words: list[str]) -> list[Token]:
    if len(understood_words) <= 0:
        return tokens
    dtokens = []
    for token in tokens:
        if token.text in understood_words:
            continue
        if token.lemma in understood_words:
            continue
        dtokens.append(token)
    return dtokens

def remove_response_duplicates(responses: list):
    if len(responses) <= 1:
        return responses

    unique_responses = []
    for response in responses:
        questions = [x.question for x in unique_responses]
        if response.question not in questions:
            unique_responses.append(response)
            
    return responses

@staticmethod
def type_checker(feats, key):
    match feats:
        case str() as feats:
            return feats
        case dict() as feats:
            return feats.get(key)
        case None as feats:
            return None
        