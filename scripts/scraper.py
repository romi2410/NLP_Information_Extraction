"""
Program to scrape data from wikipedia pages.
"""

from collections import Counter
import wikipediaapi
import re

fname = "corpus/corpus.txt"
f = open(fname, "a")

pages = ['Steve Jobs',
         'Tim Cook',
         'Steve Wozniak',
         'Jeff Bezos',
         'Mark Zuckerberg',
         'Bill Gates',
         'Stephen Hawking',
         'Larry Page',
         'Marc Benioff',
         'Paul Allen',
         'Jerry Yang',
         'Elon Musk',
         'Steve Ballmer',
         'Tim Berners-Lee',
         'Kevin Systrom',
         'Sundar Pichai',
         'Evan Spiegel',
         'Alexander Fleming',
         'Bjarne Stroustrup',
         'Jack Dorsey',
         'James Goslin',
         'Bob Iger']

wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

for page in pages:
    p_wiki = wiki_wiki.page(page)

    if p_wiki.exists():
        # Extract information till 'References' section
        p_wiki = (p_wiki.text).partition("References")[0]

        # Make sure that . is followed by a space
        p_wiki = re.sub(r'(?<=[.])(?=[^\s])', r' ', p_wiki)

        # Reference resolution
        p_wiki = re.sub(r'\bHe\b', r''+page+'', p_wiki)
        p_wiki = re.sub(r'\bhe\b', r''+page+'', p_wiki)

        f.write(p_wiki)

        print(page + " - Page exists & added to Corpus.")
    else    :
        print(page + " - Page doesn't exist.")

f.close()

wordCount = 0
with open(fname, 'r') as f:
    for line in f:
        words = line.split()
        wordCount += len(words)
f.close()
print("Corpus created with " + str(wordCount) + " words.")
