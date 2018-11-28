from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from nltk.parse.stanford import StanfordDependencyParser
#import nltk
#from nltk import CFG
##from nltk.corpus import treebank
#import nltk.parse.ProjectiveDependencyParser

def part3():
    fileName = "corpus.txt"
    with open(fileName, 'r') as corpus:
        userInput = corpus.read()
    #userInput = "A car has a door. I shot an elephant in my sleep."
#Question 1
    sentences = sent_tokenize(userInput)
    words = word_tokenize(userInput)
    print("Tokenizing the data into sentences: ", sentences)
    print("Tokenizing the sentences into words: ", words)
#Question 2
    lemmatizer = WordNetLemmatizer()
    lemmatizedData = [lemmatizer.lemmatize(word) for word in words]
    print(lemmatizedData)
#Question 3
    posTagging = pos_tag(words)
    print(posTagging)
#Question 4
    path_to_jar = 'C:/Users/praha/Downloads/stanford-parser-full-2018-10-17/stanford-parser-full-2018-10-17/stanford-parser.jar'
    path_to_models_jar = 'C:/Users/praha/Downloads/stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2-models.jar'

    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

    result = dependency_parser.raw_parse(userInput)
    dep = result.__next__()

    x = list(dep.triples())
    print(x)
#Question 5
    for d in words:
        synsetsData = wordnet.synsets(d)
        for data in synsetsData:
            print("hypernyms: ", data.hypernyms())
            print("hyponyms: ", data.hyponyms())
            print("meronyms: ", data.part_meronyms())
            print("holonyms: ", data.part_holonyms())
part3()

