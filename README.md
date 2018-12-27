
# WIKIPEDIA BASED INFORMATION EXTRACTION SYSTEM (TEMPLATE-FILLING)

## Problem Description
The purpose of this project is to extract information from unstructured data. Wikipedia provides a huge dataset to work with as it contains diverse set of terms and complex abstraction of common knowledge. We took set of Wikipedia pages on famous people in technology for the task of proper classification of entities, assignment of entities into roles and relations and drawing inferences. We represented the information as templates consisting of fixed sets of slots.

## Proposed Solution
We used template filling approach to find information from the Wikipedia corpus using python scripts and then filled the slots in the associated templates with the extracted information. The slots contain text segments extracted directly from the text and concepts that have been inferred from the text via additional processing. We divided this major task into four subtasks which are outlined below -

## Team
Romi Padam
Prahalya Reddy


## Corpus Creation
Python version: 3.6.1
Program name:  scraper.py
To run the program: Navigate to the path where python program is downloaded and create folder named ‘corpus’. Type ‘python ./scraper.py’ to run the code. 
Output: corpus.txt file will be generated with the Wikipedia data.

## Feature Extraction using NLP features
Python version: 3.6.1
Program name:  featureExtraction.py
To run the program: Navigate to the path where python program is downloaded and type ‘python ./featureExtraction.py’ to run the code. 
Output: Menu will be displayed for running deeper NLP pipeline.

## Template filling using Pattern Matching
Python version: 3.6.1
Program name:  ie.py
To run the program: 
Start the server using the following command.
java -mx3g -cp “*" edu.stanford.nlp.pipeline.StanfordCoreNLP
Navigate to the path where python program is downloaded and type ‘python ./ie.py’ to run the code. 
Output: Templates with relevant information will be displayed.





