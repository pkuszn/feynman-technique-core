from trankit import Pipeline
from dtos import DetailedWordKeyResponse

pipeline = Pipeline(lang='polish', gpu=True, cache_dir='./cache')

def process_part_of_speech(words: list[DetailedWordKeyResponse]):
    try:
        detailed_words = []
        list = pipeline(words, is_sent=True)
        for token in list['tokens']:
            detailed_words.append(DetailedWordKeyResponse(
                token['text'],
                token['lemma'],
                token['upos']
            ))
        return detailed_words
    except Exception as e:
        print(e)
