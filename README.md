
# WIKIPEDIA BASED INFORMATION EXTRACTION SYSTEM
#             (TEMPLATE-FILLING)

## Problem Description
The purpose of this project is to extract information from unstructured data. Wikipedia provides a huge dataset to work with as it contains diverse set of terms and complex abstraction of common knowledge. We took set of Wikipedia pages on famous people in technology for the task of proper classification of entities, assignment of entities into roles and relations and drawing inferences. We represented the information as templates consisting of fixed sets of slots.

## Proposed Solution
We used template filling approach to find information from the Wikipedia corpus using python scripts and then filled the slots in the associated templates with the extracted information. The slots contain text segments extracted directly from the text and concepts that have been inferred from the text via additional processing. We divided this major task into four subtasks which are outlined below -

### Task 1 : Created a set of templates and slots.
For this project, we identified semantic entities and events , and created a total of 12 information templates and 40 slots.
#### Template 1
Key_People
Key_Person_Name
Birth_Place
Birth_Date
Nationality
#### Template 2
Family
Key_Person_Name
Ancestry
Father
Mother
Children
Relatives
#### Template 3
Occupation
Key_Person_Name
Work
Board_Member_Of
#### Template 4
Education
Key_Person_Name
Year
Degree
Discipline
University
#### Template 5
Career
Key_Person_Name
Company
Title
Number_Of_Years
#### Template 6
Health
Key_Person_Name
Disability_Flag
Disability
Illness
#### Template 7
Financial_Status
Key_Person_Name
Salary
Net_Worth
Possessions
#### Template 8
Recognition
Key_Person_Name
Year
Accolade
Patents
Tributes
#### Template 9
Philanthropic_Endeavours
Key_Person_Name
Charitable Organization
Amount_Donated
#### Template 10
Death
Key_Person_Name
Place_Died
Date_Died
Cause_Of_Death
Resting_Place
#### Template 11
Publications
Key_Person_Name
Books
Papers
Films
#### Template 12
Innovations
Key_Person_Name
Entity
Year
Cofounders


### Task 2 : Created a corpus of natural language statements.
Wikipedia, in particular, is a rich source of textual data and contains vast collection of knowledge. We built a corpus from the set of English Wikipedia articles, which are freely and conveniently available online. In order to build the corpus, we used Wikipedia-API, a python wrapper for Wikipedia’s API. We wrote a python script scraper.py to built the corpus by simply scraping the data and removing References section. Our corpus comprises of 85,000 words and is built for following famous people in technology -
● Steve Jobs
● Tim Cook
● Steve Wozniak
● Jeff Bezos
● Mark Zuckerberg
● Bill Gates
● Stephen Hawking
● Larry Page
● Marc Benioff
● Paul Allen
● Jerry Yang
● Elon Musk
● Steve Ballmer
● Tim Berners-Lee
● Kevin Systrom
● Sundar Pichai
● Evan Spiegel
● Alexander Fleming
● Bjarne Stroustrup
● Jack Dorsey
● Bob Iger

A snippet from the corpus -
“Steven Paul Jobs (; February 24, 1955 – October 5, 2011) was an American business magnate and investor. Steve Jobs was the chairman, chief executive officer (CEO), and co-founder of Apple Inc. ; chairman and majority shareholder of Pixar; a member of The Walt Disney Company's board of directors following its acquisition of Pixar; and the founder, chairman, and CEO of NeXT. …”

### Task 3 : Extracted NLP based features from corpus.
We implemented a deeper NLP pipeline to extract the following NLP based features from the natural language statements.
● Tokenized the corpus into sentences and words. Using NLTK package, we segmented the entire corpus into sentences and
then tokenized the sentences into words.
● Lemmatized the words to extract lemmas as features. Using NLTK package, we lemmatized the corpus to reduce inflectional forms and sometimes derivationally related forms of a word to a common base form.
● Part-of-speech(POS) tagged the words to extract POS tag features. Using NLTK package, we classified words into their part-of-speech and label them with appropriate POS tag.
● Performed dependency parsing to identify parsed tree based patterns as features. Using Stanford dependency parser, we analyzed the grammatical structure of the sentences and established relationships between head words and words that modify those heads.
● Used WordNet to extract hypernyms, hyponyms, meronyms and holonyms as features.

### Task 4 : Filled templates from corpus.
We implemented a heuristic based approach to extract filled information templates from the corpus of natural language statements. We ran the deeper NLP pipeline (from Task 3) on the entire corpus and then, using a python script and pattern-based information extraction methods, extracted features specific to the templates.

## Programming Tools Used
● Python 3.6.1.
● Wikipedia-API (Python wrapper for Wikipedia’s API).
● Natural Language ToolKit (NLTK).
● Stanford NER Tagger.
● Anaphora Resolution.
● Stanford Dependency Parser.
● Geotext.
