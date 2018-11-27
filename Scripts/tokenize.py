

# Tokenize text into sentences

from nltk import sent_tokenize
fname = "corpus.txt"

with open(fname, 'r') as corpus:
    text = corpus.read()

sent_tokenize_list = sent_tokenize(text)
print(sent_tokenize_list)
