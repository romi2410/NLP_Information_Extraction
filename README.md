
# WIKIPEDIA BASED INFORMATION EXTRACTION SYSTEM (TEMPLATE-FILLING)

## Problem Description
The purpose of this project is to extract information from unstructured data. Wikipedia provides a huge dataset to work with as it contains diverse set of terms and complex abstraction of common knowledge. We took set of Wikipedia pages on famous people in technology for the task of proper classification of entities, assignment of entities into roles and relations and drawing inferences. We represented the information as templates consisting of fixed sets of slots.

## Proposed Solution
We used template filling approach to find information from the Wikipedia corpus using python scripts and then filled the slots in the associated templates with the extracted information. The slots contain text segments extracted directly from the text and concepts that have been inferred from the text via additional processing. We divided this major task into four subtasks which are outlined below -

### Task 1 : Created a set of templates and slots.
For this project, we identified semantic entities and events , and created a total of 12 information templates and 40 slots.
#### Template 1
Key_People&nbsp;
Key_Person_Name&nbsp;
Birth_Place&nbsp;
Birth_Date&nbsp;
Nationality&nbsp;
#### Template 2
Family&nbsp;
Key_Person_Name&nbsp;
Ancestry&nbsp;
Father&nbsp;
Mother&nbsp;
Children&nbsp;
Relatives&nbsp;
#### Template 3
Occupation&nbsp;
Key_Person_Name&nbsp;
Work&nbsp;
Board_Member_Of&nbsp;
#### Template 4
Education&nbsp;
Key_Person_Name&nbsp;
Year&nbsp;
Degree&nbsp;
Discipline&nbsp;
University&nbsp;
#### Template 5
Career&nbsp;
Key_Person_Name&nbsp;
Company&nbsp;
Title&nbsp;
Number_Of_Years&nbsp;
#### Template 6
Health&nbsp;
Key_Person_Name&nbsp;
Disability_Flag&nbsp;
Disability&nbsp;
Illness&nbsp;
#### Template 7
Financial_Status&nbsp;
Key_Person_Name&nbsp;
Salary&nbsp;
Net_Worth&nbsp;
Possessions&nbsp;
#### Template 8
Recognition&nbsp;
Key_Person_Name&nbsp;
Year&nbsp;
Accolade&nbsp;
Patents&nbsp;
Tributes&nbsp;
#### Template 9
Philanthropic_Endeavours&nbsp;
Key_Person_Name&nbsp;
Charitable Organization&nbsp;
Amount_Donated&nbsp;
#### Template 10
Death&nbsp;
Key_Person_Name&nbsp;
Place_Died&nbsp;
Date_Died&nbsp;
Cause_Of_Death&nbsp;
Resting_Place&nbsp;
#### Template 11
Publications&nbsp;
Key_Person_Name&nbsp;
Books&nbsp;
Papers&nbsp;
Films&nbsp;
#### Template 12
Innovations&nbsp;
Key_Person_Name&nbsp;
Entity&nbsp;
Year&nbsp;
Cofounders&nbsp;


### Task 2 : Created a corpus of natural language statements.
Wikipedia, in particular, is a rich source of textual data and contains vast collection of knowledge. We built a corpus from the set of English Wikipedia articles, which are freely and conveniently available online. In order to build the corpus, we used Wikipedia-API, a python wrapper for Wikipedia’s API. We wrote a python script scraper.py to built the corpus by simply scraping the data and removing References section. Our corpus comprises of 85,000 words and is built for following famous people in technology -&nbsp;
● Steve Jobs&nbsp;
● Tim Cook&nbsp;
● Steve Wozniak&nbsp;
● Jeff Bezos&nbsp;
● Mark Zuckerberg&nbsp;
● Bill Gates&nbsp;
● Stephen Hawking&nbsp;
● Larry Page&nbsp;
● Marc Benioff&nbsp;
● Paul Allen&nbsp;
● Jerry Yang&nbsp;
● Elon Musk&nbsp;
● Steve Ballmer&nbsp;
● Tim Berners-Lee&nbsp;
● Kevin Systrom&nbsp;
● Sundar Pichai&nbsp;
● Evan Spiegel&nbsp;
● Alexander Fleming&nbsp;
● Bjarne Stroustrup&nbsp;
● Jack Dorsey&nbsp;
● Bob Iger&nbsp;

A snippet from the corpus -
“Steven Paul Jobs (; February 24, 1955 – October 5, 2011) was an American business magnate and investor. Steve Jobs was the chairman, chief executive officer (CEO), and co-founder of Apple Inc. ; chairman and majority shareholder of Pixar; a member of The Walt Disney Company's board of directors following its acquisition of Pixar; and the founder, chairman, and CEO of NeXT. …”

### Task 3 : Extracted NLP based features from corpus.
We implemented a deeper NLP pipeline to extract the following NLP based features from the natural language statements.&nbsp;
● Tokenized the corpus into sentences and words. Using NLTK package, we segmented the entire corpus into sentences and
then tokenized the sentences into words.&nbsp;
● Lemmatized the words to extract lemmas as features. Using NLTK package, we lemmatized the corpus to reduce inflectional forms and sometimes derivationally related forms of a word to a common base form.&nbsp;
● Part-of-speech(POS) tagged the words to extract POS tag features. Using NLTK package, we classified words into their part-of-speech and label them with appropriate POS tag.&nbsp;
● Performed dependency parsing to identify parsed tree based patterns as features. Using Stanford dependency parser, we analyzed the grammatical structure of the sentences and established relationships between head words and words that modify those heads.&nbsp;
● Used WordNet to extract hypernyms, hyponyms, meronyms and holonyms as features.&nbsp;

### Task 4 : Filled templates from corpus.
We implemented a heuristic based approach to extract filled information templates from the corpus of natural language statements. We ran the deeper NLP pipeline (from Task 3) on the entire corpus and then, using a python script and pattern-based information extraction methods, extracted features specific to the templates.

## Programming Tools Used
● Python 3.6.1.&nbsp;
● Wikipedia-API (Python wrapper for Wikipedia’s API).&nbsp;
● Natural Language ToolKit (NLTK).&nbsp;
● Stanford NER Tagger.&nbsp;
● Anaphora Resolution.&nbsp;
● Stanford Dependency Parser.&nbsp;
● Geotext.&nbsp;
