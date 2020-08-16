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

# saving


# loading
# with open('tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)
def getStatements():
	statements = []
	for item in os.listdir('./statements/'):
		f = open('./statements/' + item)
		statements.append(f.read())
	return statements


def init():

	# GET STATEMENTS FROM FOLDER
	dandrews_statements = getStatements()
	dandrews_statements[:] = [string.replace("\n\n", " \n\n ") for string in dandrews_statements]

	# TOKENIZE THE WORDS
	tokenizer = Tokenizer(num_words=5000, filters=",\".\t:", lower=True)
	tokenizer.fit_on_texts(dandrews_statements)
	word_index = tokenizer.word_index
	total_words = len(tokenizer.word_index)+1

	input_sentances = []

	for line in dandrews_statements:
		token_list=  tokenizer.texts_to_sequences([line])[0]
		for i in range(1, len(token_list)):
			n_gram_sequence= token_list[:i+1]
			input_sentances.append(n_gram_sequence)

	max_sequences_len= max([len(x)  for x in input_sentances])
	input_sentances = np.array(pad_sequences(input_sentances, maxlen=max_sequences_len, padding='pre'))
	
	xs = input_sentances[:,:-1]
	labels = input_sentances[:,-1]

	ys = tf.keras.utils.to_categorical(labels,num_classes=total_words)

	with open('tokenizer.pickle', 'wb') as handle:
		pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

	model = Sequential()
	model.add(Embedding(total_words, 240, input_length = max_sequences_len -1))
	model.add(Bidirectional(LSTM(150)))
	model.add(Dense(total_words, activation='softmax'))
	adam = Adam(lr=0.01)
	model.compile(loss ='categorical_crossentropy',optimizer=adam, metrics=['accuracy'])
	history = model.fit(xs,ys,epochs=50,verbose=1)
	t = time.time()

	export_path_keras = "./{}.h5".format(int(t))
	print(export_path_keras)

	model.save(export_path_keras)






if __name__ == "__main__":
	init()