from trankit import Pipeline
from dtos import SpecifiedWordDto

pipeline = Pipeline(lang='polish', gpu=True, cache_dir='./cache')

def process_part_of_speech(words: list):
    try:
        processed_list = []
        list = pipeline(words, is_sent=True)
        for token in list['tokens']:
            processed_list.append(SpecifiedWordDto(
                token['text'],
                token['lemma'],
                token['upos']
            ))
        return processed_list
    except Exception as e:
        print(e)
