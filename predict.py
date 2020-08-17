import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Embedding, Bidirectional, Dense
from keras.layers.recurrent import LSTM
from keras.optimizers import Adam
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import numpy as np
import time
import pickle
import sys

with open('tokenizer.pickle', 'rb') as handle:
	tokenizer = pickle.load(handle)

def getStatements():
	statements = []
	for item in os.listdir('./statements/'):
		f = open('./statements/' + item)
		statements.append(f.read())
	return statements


def init(seed_sentance):
	# GET STATEMENTS FROM FOLDER
	# dandrews_statements = getStatements()
	# dandrews_statements[:] = [string.replace("\n\n", " \n\n ") for string in dandrews_statements]

	# # TOKENIZE THE WORDS
	# tokenizer = Tokenizer(num_words=5000, filters=",\".\t:", lower=True)
	# tokenizer.fit_on_texts(dandrews_statements)
	# word_index = tokenizer.word_index

	model = tf.keras.models.load_model('./1597594986.h5')
	next_words = 100

	for _ in range(next_words):
		token_list = tokenizer.texts_to_sequences([seed_sentance])[0]
		token_list = pad_sequences([token_list], maxlen=1037, padding='pre')
		predicted = model.predict_classes(token_list, verbose=0)
		output_word = ""
		for word, index in tokenizer.word_index.items():
			if index == predicted:
				output_word = word
				break
		seed_sentance += " " + word
		
	print(seed_sentance)

if __name__ == "__main__":
	init(sys.argv[1])