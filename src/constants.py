from enum import Enum

class PersonFeatureValueEnum(Enum):
    ZERO_PERSON = 0
    FIRST_PERSON = 1
    SECOND_PERSON = 2
    THIRD_PERSON = 3
    FOURTH_PERSON = 4
    
class PartOfSpeechEnum(Enum):
    INNE = 0
    RZECZOWNIK = 1
    PRZYMIOTNIK = 2
    LICZEBNIK = 3
    PRZYSŁÓWEK = 4
    CZASOWNIK = 5
    ZAIMEK = 6
    PRZYIMEK = 7
    SPÓJNIK = 8
    PUNKT = 9
    WYKRZYKNIK = 10
    PARTYKUŁA = 11
    ZAIMEK_WSKAZUJĄCY = 12
    CZASOWNIK_POMOCNICZY = 13
    RZECZOWNIK_ODPOWIEDNI = 14
    SPÓJNIK_KOORDYNACYJNY = 15
    SYMBOL = 16

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class PartOfSpeechConst:
    INNE = "X"
    RZECZOWNIK = "NOUN"
    PRZYMIOTNIK = "ADJ"
    LICZEBNIK = "NUM"
    PRZYSŁÓWEK = "ADV"
    CZASOWNNIK = "VERB"
    ZAIMEK = "PRON"
    PRZYIMEK = "ADP"
    SPÓJNIK = "SCONJ"
    PUNKT = "PUNCT"
    WYKRZYKNIK = "INTJ"
    PARTYKUŁA = "PART"
    ZAIMEK_WSKAZUJĄCY = "DET"
    CZASOWNIK_POMOCNICZY = "AUX"
    RZECZOWNIK_ODPOWIEDNI = "PROPN"
    SPÓJNIK_KOORDYNACYJNY = "CCONJ"
    SYMBOL = "SYM"
    
def part_of_speech_mapper(arg):
    match arg:
        case "X": 
           return 0
        case "NOUN": 
            return 1
        case "ADJ": 
            return 2
        case "NUM": 
            return 3
        case "ADV": 
            return 4
        case "VERB": 
            return 5
        case "PRON": 
            return 6
        case "ADP": 
            return 7
        case "SCONJ": 
            return 8
        case "PUNCT": 
            return 9
        case "INTJ": 
            return 10
        case "PART": 
            return 11
        case "DET": 
            return 12
        case "AUX": 
            return 13
        case "PROPN": 
            return 14
        case "CCONJ": 
            return 15
        case "SYM": 
            return 16
        case _: 
            return 0
        
class NumberFeatureValueConst:
    SingularNumber = "Sing"
    PluralNumber = "Plur"
    
class TypoFeatureValueConst:
    IsTypo = "Yes"

class GenderFeatureValueConst:
    Masculine = "Masc"
    Feminine =  "Fem"
    Neuter = "Neut"
    Common = "Com"

class UniversalFeaturesConst:
    PronType = "PronType"
    NumType = "NumType"
    Poss = "Poss"
    Reflex = "Reflex"
    Foreign = "Foreign"
    Abbr = "Abbr"
    Typo = "Typo"
    Gender = "Gender"
    Animacy = "Animacy"
    NounClass = "NounClass"
    Number = "Number"
    Case = "Case"
    Definite = "Definite"
    Degree = "Degree"
    VerbForm = "VerbForm"
    Mood = "Mood"
    Tense = "Tense"
    Aspect = "Aspect"
    Voice = "Voice"
    Evident = "Evident"
    Polarity = "Polarity"
    Person = "Person"
    Polite = "Polite"
    Clusivity = "Clusivity"

class AnimacyFeatureValueConst:
    Animate = "Anim"
    Inanimate = "Inan"
    Human = "Hum"
    NonHuman = "Nhum"
    
class DependencyParsingConst:
    AMOD = 'amod'
    ADVMOD_NEG = 'advmod:neg'
    NMOD = 'nmod'
    
class PointedVerbs:
    POINTED_LIST = ['być', 'wyrażać', 'oznaczać', 'znaczyć', 'cechować', 'to']