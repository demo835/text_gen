

import spacy
import gensim
# from gensim import corpora, models, similiarities

text = open(u"input.txt", mode='r').read()

doc = nlp(text.lower())

# tok_corp = [nltk.word_tokenize(sent.decode('utf-8')) for sent in text]

# model = gensim.models.Word2Vec(tok_corp, min_count = 1, size = 32)

# print(model.most_similiar('heart'))