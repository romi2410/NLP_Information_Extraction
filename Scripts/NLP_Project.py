from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

def part3():
    userInput = input("Enter a sentence(s): ")
    sentences = sent_tokenize(userInput)
    words = word_tokenize(userInput)
    print("Tokenizing the data into sentences: ", sentences)
    print("Tokenizing the sentences into words: ", words)

    lemmatizer = WordNetLemmatizer()
    lemmatizedData = [lemmatizer.lemmatize(word) for word in words]
    print(lemmatizedData)

    for d in lemmatizedData:
        synsetsData = wordnet.synsets(d)
        for data in synsetsData:
            print("hypernyms: ", data.hypernyms())
part3()
