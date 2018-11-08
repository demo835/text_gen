from _utils import startup
import logging

import spacy
import gensim
from gensim import corpora, models, similarities
from gensim.test.utils import common_corpus, common_dictionary
from gensim.models import Word2Vec

# from gensim import corpora, models, similiarities

startup()

t = open(u"input.txt", mode='r').read()
logging.debug("Length of text is :", len(t))

nlp = spacy.load('en_core_web_lg')
nlp.max_length = 2000000

doc = nlp(t.lower())

tok_corp = []
for word in doc:
    tok_corp.append([word.text])

# print(tok_corp)



# dictionary = corpora.Dictionary(tok_corp)
# print(tok_corp)
# lsi = models.LsiModel(tok_corp, id2word=dictionary, num_topics=300)

# index = similarities.Similarity(lsi[corpus])


# test = "sword"
# vec_bow = dictionary.doc2bow(doc.lower().split())
# vec_lsi = lsi[vec_bow]

# sims = index[vec_lsi]

# sims = sorted(enumerate(sims), key=lambda item: -item[1])
# print(sims)
# model = gensim.models.Word2Vec(tok_corp, min_count = 1, size = 32, sg = 1, window = 3)
model = Word2Vec(tok_corp, size = 64, sg = 1, window = 3)
model.save("first.model")

print(model.wv.most_similar('gaunt'))


# model = gensim.models.Word2Vec.load("./first.model")
