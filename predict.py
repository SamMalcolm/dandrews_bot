import pickle


with open('tokenizer.pickle', 'rb') as handle:
	tokenizer = pickle.load(handle)