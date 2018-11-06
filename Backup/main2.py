'''Example script to generate text from Nietzsche's writings.
At least 20 epochs are required before the generated text
starts sounding coherent.
It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.
If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''
from __future__ import print_function
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM, Input, Flatten, Bidirectional
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.metrics import categorical_accuracy
import numpy as np
import random
import sys
import os
import time
import codecs
import collections

# from __future__ import print_function
from keras.callbacks import LambdaCallback
# from keras.models import Sequential
# from keras.layers import Dense, Activation
# from keras.layers import LSTM
# from keras.optimizers import RMSprop
# from keras.utils.data_utils import get_file
# import numpy as np
# import random
# import sys
# import io

# initialize the output text file
file_output = open("./output.txt", "w")

# open the trainer file, data is already prepared
file_input = open("./source-pirates-prepared.txt")
text = file_input.read().lower()
print('corpus length:', len(text))

# path = get_file(
#     'Source - Pirates.txt',
#     origin='./Source - Pirates.txt')
# with io.open(file_object, encoding='utf-8') as f:
#     text = f.read().lower()
# print('corpus length:', len(text))

chars = sorted(list(set(text)))
print('total chars:', len(chars))
print("List of characters: ", chars)
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

# transform the words in numbers
print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


# build the model: a single LSTM
# print('Build model...')
# model = Sequential()
# model.add(LSTM(128, input_shape=(maxlen, len(chars))))
# model.add(Dense(len(chars)))
# model.add(Activation('softmax'))

# optimizer = RMSprop(lr=0.01)
# model.compile(loss='categorical_crossentropy', optimizer=optimizer)

print('Build LSTM model.')
model = Sequential()
model.add(Bidirectional(LSTM(128, activation="relu"),input_shape=(maxlen, len(chars))))
model.add(Dropout(0.6))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))
    
optimizer = Adam(lr=0.01)
callbacks=[EarlyStopping(patience=2, monitor='val_loss')]
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=[categorical_accuracy])

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    # print("Beginning of sample function.")
    # print("preds: ", preds)
    # print("temperature: ", temperature)
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def on_epoch_end(epoch, logs):
    # Function invoked at end of each epoch. Prints generated text.
    print()
    print('----- Generating text after Epoch: %d' % epoch)

    start_index = random.randint(0, len(text) - maxlen - 1)
    # Check start_index and ensure that it lands at the beginning of a word, not in the middle of one
    while text[start_index] != " ":
        start_index = start_index - 1

    for diversity in [0.2, 0.3]:
    # for diversity in [0.2, 0.3, 0.8, 1.0]:
        print('----- diversity:', diversity)

        generated = ''
        sentence = text[start_index: start_index + maxlen]
        generated += sentence
        print('----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)
        file_output.write(generated)

        # this predicts 400 new characters
        for i in range(400):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            file_output.write(next_char)
            sys.stdout.flush()
        print()

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

model.fit(x, y,
          batch_size=128,
          epochs=60,
          callbacks=[print_callback])