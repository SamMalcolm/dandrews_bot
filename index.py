import tensorflow as tf 
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer

def getStatements():
	print(True)

def init():
	getStatements()
	dandrews_statements = ["You can't stay home if you don't have one.\n\nAnd you can't wash your hands and protect yourself if you don't have access to soap and water.\n\nThis pandemic has laid bare some of the deepest inequalities in our society – not least the need for secure housing."]
	dandrews_statements[:] = [string.replace("\n\n", "\n\n\t") for string in dandrews_statements]
	print(dandrews_statements)
	tokenizer = Tokenizer(num_words=10000, filters=".\t", lower=True)
	tokenizer.fit_on_texts(dandrews_statements)
	word_index = tokenizer.word_index
	print(word_index)

if __name__ == "__main__":
	init()