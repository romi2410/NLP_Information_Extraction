"""
Program to scrape data from wikipedia pages.
"""

from collections import Counter
import wikipediaapi

fname = "corpus.txt"
f = open(fname, "a")

pages = ['Steve Jobs',
         'Tim Cook',
         'Steve Wozniak',
         'Jeff Bezos',
         'Mark Zuckerberg',
         'Bill Gates',
         'Stephen Hawking',
         'Larry Page']

wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

for page in pages:
    p_wiki = wiki_wiki.page(page)

    if p_wiki.exists():
        f.write(p_wiki.text)
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
