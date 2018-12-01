"""
Script to implement deeper NLP pipeline. The script extracts following NLP based features
from the natural language statements.

1. Tokenize the input into sentences and words.
2. Lemmatize the words to extract lemmas as features.
3. Part-of-speech(POS) tag the words to extract POS tag features.
4. Perform dependency parsing to parse tree based patterns as features.
5. Extract hypernyms, hyponyms, meronyms and holonyms as features.
"""

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.parse.stanford import StanfordDependencyParser

# Implementation of a tokenizer to divide strings into lists of substrings
def tokenize(s):
    # Split string into sentences
    print("\n\nSentence Tokenizer:")
    print(sent_tokenize(s))
    # Split string into words
    print("\nWord Tokenizer:")
    print(word_tokenize(s))

# Implementation of a lemmatizer to reduce inflectional forms to a common base form.
def lemmatize(s):
    print("\n\nLemmatizer: ")
    wordnet_lemmatizer = WordNetLemmatizer()
    print([wordnet_lemmatizer.lemmatize(word) for word in word_tokenize(s)])

# Part-of-speech tagging to classify words into their lexical categories.
def posTag(s):
    print("\n\nPOS Tagging:")
    print(pos_tag(word_tokenize(s)))

# Parse sentences using StanfordDependencyParser.
def syntacticParse(s):
    stanford_parser_dir = 'libraries/'
    my_path_to_models_jar = stanford_parser_dir  + "stanford-corenlp/stanford-corenlp-3.9.2-models.jar"
    my_path_to_jar = stanford_parser_dir  + "stanford-parser/stanford-parser.jar"

    dependency_parser = StanfordDependencyParser(path_to_jar=my_path_to_jar, path_to_models_jar=my_path_to_models_jar)
    result = dependency_parser.raw_parse(s)
    print(list((result.__next__()).triples()))

def extractRelations(s):
    

if __name__ == "__main__":

    string = input("Enter string: ")

    while True:
        # Printing menu
        print("""
        1. Tokenize the input into sentences and words.
        2. Lemmatize the words to extract lemmas as features.
        3. Part-of-speech(POS) tag the words to extract POS tag features.
        4. Perform dependency parsing to parse tree based patterns as features.
        5. Extract hypernyms, hyponyms, meronyms and holonyms as features.
        6. Exit.
        """)

        inp = input("\n\nWhat would you like to do? ")

        if inp == "1":
            tokenize(string)
        elif inp == '2':
            lemmatize(string)
        elif inp == '3':
            posTag(string)
        elif inp == '4':
            syntacticParse(string)
        elif inp == '5':
            extractRelations(string)
        elif inp == "6":
            print("\nGoodbye!")
            exit()
        else:
            print("\n Not Valid Choice! Try again.")
