import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOPS = set(stopwords.words("english"))

def clean(text: str) -> list:
    tokens = word_tokenize(text.lower())
    return [t for t in tokens if t.isalpha() and t not in STOPS]