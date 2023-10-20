import logging
from trankit import Pipeline
from dtos import Token
from models import TokenResponse
from constants import (
    DependencyParsingConst, 
    PartOfSpeechConst, 
    PointedVerbs
)

pipeline = Pipeline(lang='polish', gpu=True, cache_dir='./cache')
ftcore_logger = logging.getLogger("ftcore")

def process_part_of_speech(words: list[str]) -> list[TokenResponse]:
    try:
        detailed_words = []
        list = pipeline(words, is_sent=True)
        for token in list['tokens']:
            detailed_words.append(TokenResponse(
                name=token['text'],
                lemma=token['lemma'],
                part_of_speech=token['upos']
            ))
        return detailed_words
    except Exception as e:
        print(e)

def try_process(data: list[str]) -> list[Token]:
    try:
        tokens = []
        output = pipeline(data)
        for sentence in output['sentences']:
            for token in sentence['tokens']:
                if 'lemma' not in token and 'expanded' in token:
                    for expand in token['expanded']:
                        if expand['lemma'] == 'być':
                            continue 
                        create_new_token(tokens, expand)
                    continue                                    
                create_new_token(tokens, token)
        log_result(tokens)
        return tokens
    except Exception as e:
        print(e)

def create_new_token(tokens: list[Token], token: Token):
    dict_feats = create_feats(token['feats']) if 'feats' in token else None
    tokens.append(Token(
                    token['id'], 
                    token['text'], 
                    token['lemma'], 
                    token['upos'], 
                    token['head'], 
                    token['deprel'],
                    dict_feats))
    
def create_feats(feats: str) -> dict:
    split_by_vertical_line_list = feats.split("|")
    feats_dict = dict()
    for item in split_by_vertical_line_list:
        eq_splited = item.split("=")
        feats_dict[eq_splited[0]] = eq_splited[1]
    return feats_dict

def create_dependencies(tokens: list[Token]) -> list[Token]:
    if len(tokens) <= 1:
        return tokens
    for root in tokens:
        match root.deprel:
            case DependencyParsingConst.AMOD:
                for child in tokens:
                    prepare_tokens_to_build_complex_questions(root, child)
            case DependencyParsingConst.NMOD:
                for child in tokens:
                    prepare_tokens_to_build_complex_question_only_nouns(root, child)
    return tokens 

def prepare_tokens_to_build_complex_questions(root: Token, child: Token):
    if root.head == child.internal_id:
        child.child.append(root)
        root.root = child
        set_complex(root, child)
        
def prepare_tokens_to_build_complex_question_only_nouns(root: Token, child: Token):
    if root.head == child.internal_id and child.upos == PartOfSpeechConst.RZECZOWNIK:
        child.child.append(root)
        root.root = child
        set_complex(root, child)

def skip_currently_explained_words(tokens: list[Token]) -> list[Token]:
    if len(tokens) <= 0:
        return None
    
    first_sentences_list = []
    id_tokens = []
    
    for token in tokens:
        if token.upos == "PUNCT":
            break
        first_sentences_list.append(token)
    
    if len(first_sentences_list) <= 0:
        return tokens
    
    try:
        root_token = next(filter(lambda x: x.head == 0, first_sentences_list))   
    except StopIteration as si:
        ftcore_logger.error(si)
        return tokens
    
    lemmas_list = [token.lemma for token in first_sentences_list]
    lemmas_set = set(lemmas_list)
    pointed_verbs_set = set(PointedVerbs.POINTED_LIST)
        
    if not (lemmas_set.intersection(pointed_verbs_set)):
        return tokens
    
    pointing_token_list = []
    for first_sentence_token in first_sentences_list:
        if first_sentence_token.head == 0:
            id_tokens.append(root_token.internal_id)
            break
        pointing_token_list.append(first_sentence_token)
    
    #TODO:temporary
    for pointing_token in pointing_token_list:
        if pointing_token.head == pointing_token.head in id_tokens:
            id_tokens.append(pointing_token.internal_id)
        for another_poiting_token in pointing_token_list:
            if another_poiting_token.head == another_poiting_token.head in id_tokens:
                id_tokens.append(another_poiting_token.internal_id)
        
    id_tokens_set = set(id_tokens)
                
    if len(id_tokens_set) <= 0:
        return tokens

    explained_tokens = []
    for token in first_sentences_list:
        if token.internal_id in id_tokens_set:
            explained_tokens.append(token)
    
    for token in tokens:
        if token in explained_tokens:
            token.status = True
    
    return tokens
        
@staticmethod
def set_complex(child: Token, root: Token):
    child.complex = True
    root.complex = True
    
@staticmethod
def log_result(tokens: list[Token]):
    if tokens == None or len(tokens) <= 0:
        return 
    for token in tokens:
        ftcore_logger.info(token.__str__())