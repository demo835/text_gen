# from __future__ import print_function
# from keras.callbacks import LambdaCallback
# from keras.models import Sequential
# from keras.layers import Dense, Activation
# from keras.layers import LSTM
# from keras.optimizers import RMSprop
# from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import io
import collections
from collections import Counter
import os
import sys

text = ""
word_to_id = ""

# initialize the output text file
file_output = open("./output.txt", "w")

# open the trainer file, data is already prepared
def read_text():
    print("In read_text function.")
    file_input = open("./input.txt")
    text = file_input.read().lower()
    print('corpus length:', len(text))
    return text

def build_vocab(text):
    print("In build_vocab function")
    counter = collections.Counter(text)
    print("Unique words in corpus: ")
    # print(Counter(counter).items())
    for k, v in counter.items():
        print(k, v)
    
    count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

    words, _ = list(zip(*count_pairs))
    word_to_id = dict(zip(words, range(len(words))))
    print("word_to_id is: ", word_to_id)

    return word_to_id


def file_to_word_ids(text, word_to_id):
    print("In file_to_word_ids function.")
    return [word_to_id[word] for word in text if word in word_to_id]

def processed():
    text = read_text()
    word_to_id = build_vocab(text)
    train_data = file_to_word_ids(text, word_to_id)
    vocabulary = len(word_to_id)
    print("vocabulary is ", vocabulary)
    print("train_data is ", train_data)

processed()

