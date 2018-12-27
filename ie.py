"""
Wikipedia Based Inforamtion Extraction By Template-fillingself.
"""

import nltk
import re
from string import Template
from geotext import GeoText
from collections import OrderedDict
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag, ne_chunk, ne_chunk_sents, RegexpParser
from nltk.tree import *
from nltk.tag.stanford import StanfordNERTagger
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

def preprocess(document):
    sentences = sent_tokenize(document)
    tokens = [word_tokenize(sent) for sent in sentences]
    posTaggedSentence = [pos_tag(sent) for sent in tokens]
    chunkedSentences = ne_chunk_sents(posTaggedSentence)
    return sentences, tokens, posTaggedSentence, chunkedSentences

def splitPOS(word):
    sep = '/'
    result = ''
    for w in word.split():
        result += w.split(sep, 1)[0]
        result += ' '
    return(result.strip())

def printTemplate(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         printTemplate(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def getOccupation(chunked_sentences):
    occupationRelations = []
    roles = """
    (.*(
    analyst|
    author|
    business\smagnate|
    chair(wo)?man|
    cofounder|
    commissioner|
    counsel|
    cosmologist|
    economist|
    editor|
    executive|
    entrepreneur|
    engineer|
    foreman|
    founder|
    governor|
    humanitarian|
    investor|
    inventor|
    lawyer|
    librarian).*)|
    manager|
    operating\sofficer|
    partner|
    president|
    progammer|
    philanthropist|
    producer|
    professor|
    researcher|
    spokes(wo)?man|
    theoretical\sphysicist|
    writer|
    ,\sof\sthe?\s*  # "X, of (the) Y"
    """
    ROLES = re.compile(roles, re.VERBOSE)
    for doc in chunked_sentences:
        for rel in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='ace', pattern=ROLES):
            occupation = ''
            for word in rel['filler'].split():
                a = word.split('/', 1)[1]
                if a in ["NN", "JJ", ',', 'CC']:
                    if a in [',', 'CC'] and occupation == '':
                        continue
                    else:
                        occupation += word.split('/', 1)[0]
                        occupation += ' '
            occupationRelations.append([splitPOS(rel['subjtext']), occupation.strip()])
    return occupationRelations

#---------------------------------------------------------------------------#
#----------------------------Template 1-------------------------------------#
#---------------------------------------------------------------------------#
#Key_People
def getBirthPlace(chunkedSentences):
    birthRelations = []
    birthPlace = re.compile(r'.*\bborn\b.*')

    for doc in chunkedSentences:
        for rel in nltk.sem.extract_rels('PER', 'GPE', doc, corpus = 'ace', pattern = birthPlace):
            if GeoText(rel['objtext']).cities:
                birthRelations.append([splitPOS(rel['subjtext']), splitPOS(rel['objtext'])])
    return birthRelations

#Key_People
def getBirthDate(sentences):
    birthDateRel = []

    birth = r"""
    FOUND: {<NNP>*<VBD>?<VBN><IN|PERSON|CC>*<NNP> <CD> <,> <CD>*}
      """
    cp = nltk.RegexpParser(birth)
    for sent in sentences:
        tree = cp.parse(sent)
        newtree = ParentedTree.convert(tree)
        for subtree in newtree.subtrees():
            if subtree.label() == 'FOUND':
                for token, pos in sent:
                    if (token == "born"):
                        string = (str(subtree)).partition("/")[2]
                        if string[:3] == "NNP":
                            st = ((str(subtree)).partition("/")[0]).partition(" ")[2]
                            birthDateRel.append([st.strip(), splitPOS(string.partition("on")[2])])
    return birthDateRel

#Key_People
def getNationality(document):
    sentences = sent_tokenize(document)
    nationalityRelations = []
    newList = []
    nationsList = ['American', 'Chinese', 'Taiwanese-American', 'English', 'British', 'Indian', 'Russian', 'Korean', 'African', 'Indian-American','Scottish']
    for i in range(len(sentences)):
        newSent = pos_tag(word_tokenize(sentences[i]))
        newList.append(newSent)
    nationalityFactor = r"""
                    NATIONALITY: {<NNP>+<.|..|NNP|CD|\,|JJ>*<VBZ><DT><JJ><NN>*}
                    """
    cp = nltk.RegexpParser(nationalityFactor)
    for s in newList:
        tree = cp.parse(s)
        for subtree in tree.subtrees():
            value = ""
            nameList = []
            wordTagList = []
            keyname = []
            native = []
            keyPerson = ''
            nation = ''
            treeExtract = ''
            if subtree.label() == 'NATIONALITY':
                treeExtract = subtree.pos()
                for w, t in treeExtract:
                    wordTagList.append(w)
                for chunk in ne_chunk(wordTagList):
                    if hasattr(chunk, 'label'):
                        nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
                for tag, word in nameList:
                    if tag == 'PERSON':
                        keyname.append(word)
                    if tag == 'GPE':
                        if word in nationsList:
                            native.append(word)
                for k in range(len(keyname)):
                    if k == 0:
                        keyPerson = keyname[0]
                    elif k > 0:
                        break
                for n in range(len(native)):
                    if n == 0:
                        nation = native[0]
                    elif n > 0:
                        break
                if not keyPerson == '':
                    if not nation == '':
                        nationalityRelations.append([keyPerson,nation])
    #print(nationalityRelations)
    return nationalityRelations

#---------------------------------------------------------------------------#
#----------------------------Template 2-------------------------------------#
#---------------------------------------------------------------------------#
#Family
def getSpouse(chunkedSentences):
    spouseRelations = []
    spouse = re.compile(r'.*\bmarried\b.*')

    for doc in chunkedSentences:
        for rel in nltk.sem.extract_rels('PER', 'PER', doc, corpus = 'ace', pattern = spouse):
            spouseRelations.append([splitPOS(rel['subjtext']), splitPOS(rel['objtext'])])
    return spouseRelations

#Family
def getAncestry(document):
    sentences = sent_tokenize(document)
    ancestryRelations = []
    ancestrySentences = []
    newList = []
    wordsList = ['ancestors', 'ancestry']
    for value in wordsList:
        wordStructure = r'.*\b'+value+'\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                ancestrySentences.append(sent)
    for i in range(len(ancestrySentences)):
        newSent = pos_tag(word_tokenize(ancestrySentences[i]))
        newList.append(newSent)
    for s in newList:
        nameList = []
        keyname = []
        ancname = []
        keyPerson = ''
        for chunk in ne_chunk(s):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        for tag, word in nameList:
            if tag == 'PERSON':
                keyname.append(word)
            if tag == 'GPE':
                ancname.append(word)
        for k in range(len(keyname)):
            if k == 0:
                keyPerson = keyname[0]
            elif k > 0:
                break
        if keyPerson.strip() is not '':
            if len(ancname) > 0:
                ancestryRelations.append([keyPerson, ancname])
    return ancestryRelations

#Family
def getRelatives(document):
    sentences = sent_tokenize(document)
    familyRelations = []
    familySentences = []
    newList = []
    wordsList = ['sister', 'brother']
    for value in wordsList:
        wordStructure = r'.*\b'+value+'.\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                familySentences.append(sent)
    for i in range(len(familySentences)):
        newSent = pos_tag(word_tokenize(familySentences[i]))
        #print(newSent)
        #print("\n \n")
        newList.append(newSent)
    for s in newList:
        nameList = []
        keyname = []
        relative = []
        keyPerson = ''
        for chunk in ne_chunk(s):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        for tag, word in nameList:
            if tag == 'PERSON':
                keyname.append(word)
        for k in range(len(keyname)):
            if k == 0:
                keyPerson = keyname[0]
            elif k > 0:
                relative.append(keyname[k])

        if len(relative) > 0:
            familyRelations.append([keyPerson, relative])
    #print(familyRelations)
    return familyRelations

#Family
def getChildren(document):
    sentences = sent_tokenize(document)
    childRelations = []
    childSentences = []
    newList = []
    wordsList = ['children', 'sons', 'daughters']
    for value in wordsList:
        wordStructure = r'.*\b'+value+'\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                childSentences.append(sent)
    for i in range(len(childSentences)):
        newSent = pos_tag(word_tokenize(childSentences[i]))
        newList.append(newSent)

    for s in newList:
        nameList = []
        keyname = []
        childrenValue = ''
        finalName = ''
        for chunk in ne_chunk(s):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        for tag, word in nameList:
            if tag == 'PERSON':
                keyname.append(word)
        if keyname:
            finalName = keyname[0]
        for i in range(len(s)-1):
            if (s[i+1][0] == 'children') and (s[i][1] == 'CD'):
                childrenValue = s[i][0]

        if finalName.strip() is not '':
            if childrenValue.strip() is not '':
                childRelations.append([finalName, childrenValue])
    return childRelations

#Family
def getParents(document):
    sentences = sent_tokenize(document)
    parentRelations = []
    parentSentences = []
    newList = []
    for sent in sentences:
        if re.search(r'.*\bborn\b.*\bto\b.*', sent):
            parentSentences.append(sent)
    wordsList = ['parents', 'father', 'mother', 'parent', 'son of']
    for value in wordsList:
        wordStructure = r'.*\b'+value+'\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                parentSentences.append(sent)
    for i in range(len(parentSentences)):
        newSent = pos_tag(word_tokenize(parentSentences[i]))
        newList.append(newSent)

    parentsFactor = r"""
                REL: {<NNP>+<VBD><VBN><TO><.><NNP>+<CC>?<NNP>}
                REL: {<NNP>+<VBZ><DT><NN><IN><.><NNP>+<CC>?<NNP>}
                """
    cp = nltk.RegexpParser(parentsFactor)
    for s in newList:
        tree = cp.parse(s)
        for subtree in tree.subtrees():
            treeExtract = []
            keyname = []
            nameList = []
            wordTagList = []
            if subtree.label() == 'REL':
                treeExtract = subtree.pos()
            for w, t in treeExtract:
                wordTagList.append(w)

            for chunk in ne_chunk(wordTagList):
                if hasattr(chunk, 'label'):
                    nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))

            for tag, word in nameList:
                if tag == 'PERSON':
                    keyname.append(word)


            for i in range(len(keyname)):
                if i ==2:
                    parentRelations.append([keyname[0],keyname[1],keyname[2]])
                elif i == 1:
                    for t, w in nameList:
                        if w == 'father':
                            if [keyname[1],keyname[0],''] not in parentRelations:
                                parentRelations.append([keyname[1],keyname[0],''])
                        elif w == 'mother':
                            if [keyname[1],'',keyname[0]] not in parentRelations:
                                parentRelations.append([keyname[1],'',keyname[0]])
                        else:
                            if [keyname[0],keyname[1],''] not in parentRelations:
                                parentRelations.append([keyname[0],keyname[1],''])
    return parentRelations
#---------------------------------------------------------------------------#
#----------------------------Template 3-------------------------------------#
#---------------------------------------------------------------------------#
#Occupation
def getOccupation(chunkedSentences):
    occupationRelations = []
    roles = """
    (.*(
    analyst|
    author|
    business\smagnate|
    chair(wo)?man|
    cofounder|
    commissioner|
    counsel|
    cosmologist|
    economist|
    editor|
    executive|
    entrepreneur|
    engineer|
    foreman|
    founder|
    governor|
    humanitarian|
    investor|
    inventor|
    lawyer|
    librarian).*)|
    manager|
    operating\sofficer|
    partner|
    president|
    progammer|
    philanthropist|
    producer|
    professor|
    researcher|
    spokes(wo)?man|
    theoretical\sphysicist|
    writer|
    ,\sof\sthe?\s*  # "X, of (the) Y"
    """
    ROLES = re.compile(roles, re.VERBOSE)
    for doc in chunkedSentences:
        for rel in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='ace', pattern=ROLES):
            occupation = ''
            for word in rel['filler'].split():
                a = word.split('/', 1)[1]
                if a in ["NN", "JJ", ',', 'CC']:
                    if a in [',', 'CC'] and occupation == '':
                        continue
                    else:
                        occupation += word.split('/', 1)[0]
                        occupation += ' '
            occupationRelations.append([splitPOS(rel['subjtext']), occupation.strip()])
    return occupationRelations

#Occupation
def getBoardMember(chunkedSentences):
    boardRelations = []

    for sent in chunkedSentences:
        if 'board' in str(sent) and 'PERSON' in str(sent) and 'ORGANIZATION' in str(sent):
            person = splitPOS((re.search(r"(PERSON.*)", str(sent)).group(0))[7:-1])
            org = splitPOS((re.search(r"(ORGANIZATION.*)", str(sent)).group(0))[13:-1])
            if 'CEO' not in org:
                boardRelations.append([person, org])
    return boardRelations

#---------------------------------------------------------------------------#
#----------------------------Template 4-------------------------------------#
#---------------------------------------------------------------------------#
#Education
def getEducation(document):
    sentences = sent_tokenize(document)
    educationRelations = []
    educationSentences = []
    words = ['graduated', 'earned', 'studied', 'enrolled', 'education']
    degreesList = ['MBBS', 'Master of Science', 'PhD', 'BA (Hons.) degree','Bachelor of Science (B.S.)', 'Master of Business Administration (MBA)', 'Bachelor of Science', 'Master of Business Administration', 'bachelor of arts', 'Bachelor of Technology', 'BA', 'M.A.','BTech', 'management science']
    disciplinesList = ['metallurgical engineering', 'applied physics', 'material sciences', 'computer engineering', 'physics', 'psychology', 'engineer', 'industrial engineering', 'electrical engineering', 'applied mathematics', 'economics', 'computer science', 'technology', 'chemistry']
    for value in words:
        wordStructure = r'.*\b'+value+'.\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                educationSentences.append(sent)


    for s in educationSentences:
        yearStructure = r'.*\b\d{4}\b.*'
        nameList = []
        keyname = []
        orgname = []
        keyPerson = ''
        universityName = []
        yearOfEducation = ''
        degreesEarned = []
        disciplines = []

        for disc in disciplinesList:
            discStructure = r'.*\b'+disc+'\\b.*'
            if re.search(discStructure, s):
                disciplines.append(disc)

        for degree in degreesList:
            degreeStructure = r'.*\b'+degree+'\\b.*'
            if re.search(degreeStructure, s):
                degreesEarned.append(degree)

        newSent = pos_tag(word_tokenize(s))
        for words, tags in newSent:
            if tags == 'CD':
                if re.search(yearStructure, words):
                    yearOfEducation = words

        for chunk in ne_chunk(newSent):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))

        for tag, word in nameList:
            if tag == 'PERSON':
                keyname.append(word)
            if tag == 'ORGANIZATION':
                orgname.append(word)
        universityName = orgname
        for k in range(len(keyname)):
            if k == 0:
                keyPerson = keyname[0]
            elif k > 0:
                break
        if keyPerson is not '':
            if len(universityName) > 0:
                if (len(degreesEarned) > 0) or (len(disciplines) > 0) or (yearOfEducation is not ''):
                    educationRelations.append([keyPerson, yearOfEducation, degreesEarned, disciplines, universityName])
   # print(educationRelations)
    return educationRelations
#---------------------------------------------------------------------------#
#----------------------------Template 5-------------------------------------#
#---------------------------------------------------------------------------#
#Career
def getCareer(chunkedSentences):
    careerRelations = []
    roles = """
    (.*(
    analyst|
    author|
    business\smagnate|
    chair(wo)?man|
    cofounder|
    commissioner|
    counsel|
    cosmologist|
    director|
    economist|
    editor|
    executive|
    entrepreneur|
    engineer|
    foreman|
    founder|
    governor|
    humanitarian|
    investor|
    inventor|
    lawyer|
    librarian).*)|
    manager|
    operating\sofficer|
    partner|
    president|
    progammer|
    philanthropist|
    producer|
    professor|
    researcher|
    spokes(wo)?man|
    theoretical\sphysicist|
    writer|
    ,\sof\sthe?\s*  # "X, of (the) Y"
    """
    ROLES = re.compile(roles, re.VERBOSE)
    for doc in chunkedSentences:
        for rel in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='ace', pattern=ROLES):
            if [splitPOS(rel['subjtext']), splitPOS(rel['objtext'])] not in careerRelations:
                occupation = ''
                for word in rel['filler'].split():
                    a = word.split('/', 1)[1]
                    if a in ["NN", "JJ", ',', 'CC']:
                        if a in [',', 'CC'] and occupation == '':
                            continue
                        else:
                            occupation += word.split('/', 1)[0]
                            occupation += ' '
                careerRelations.append([splitPOS(rel['subjtext']), splitPOS(rel['objtext']), occupation, ' '])

        spent = re.compile(r'.*\bspent\b.*')

        for rel in nltk.sem.extract_rels('PER', 'ORG', doc, corpus = 'ace', pattern = spent):

            occupation = ''
            for word in rel['filler'].split():
                a = word.split('/', 1)[1]
                if a in ["NN", "JJ", ',', 'CC']:
                    if a in [',', 'CC'] and occupation == '':
                        continue
                    else:
                        occupation += word.split('/', 1)[0]
                        occupation += ' '

            for word in (rel['filler']).split():
                if 'CD' in word:
                    year = splitPOS(word)
                    #print(year)
                    for a in careerRelations:
                        if splitPOS(rel['subjtext']) == a[0] and splitPOS(rel['objtext']) == a[1]:
                            careerRelations.remove(a)
                            careerRelations.append([splitPOS(rel['subjtext']), splitPOS(rel['objtext']), occupation, year])
                        else:
                            careerRelations.append([splitPOS(rel['subjtext']), splitPOS(rel['objtext']), occupation, year])

    return careerRelations

#---------------------------------------------------------------------------#
#----------------------------Template 6-------------------------------------#
#---------------------------------------------------------------------------#
#Health
def getDisability(document):
    sentences = sent_tokenize(document)
    disabilityRelations = []
    disabilitySentences = []
    newList = []
    wordsList = ['disability', 'paralyzed']
    for value in wordsList:
        wordStructure = r'.*\b'+value+'\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                disabilitySentences.append(sent)

    for i in range(len(disabilitySentences)):
        newSent = pos_tag(word_tokenize(disabilitySentences[i]))
        newList.append(newSent)

    for s in newList:
        value = ""
        nameList = []
        keyname = []
        finalName = ""
        for chunk in ne_chunk(s):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        for tag, word in nameList:
            if tag == 'PERSON':
                keyname.append(word)
        if keyname:
            finalName = keyname[0]
        if finalName.strip() is not '':
            disabilityRelations.append(finalName)
    return disabilityRelations

#Health
def getIllnessRelations(document):
    sentences = sent_tokenize(document)
    illnessRelations = []
    illnessSentences = []
    newList = []
    wordsList = ['suffering', 'disease', 'diagnosed', 'illness']
    for value in wordsList:
        wordStructure = r'.*\b'+value+'\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                illnessSentences.append(sent)

    for i in range(len(illnessSentences)):
        newSent = pos_tag(word_tokenize(illnessSentences[i]))
        newList.append(newSent)

    for s in newList:
        value = ""
        nameList = []
        keyname = []
        wordTagList = []
        illnessValue = ""
        finalName = ""
        for chunk in ne_chunk(s):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        for tag, word in nameList:
            if tag == 'PERSON':
                keyname.append(word)
        if keyname:
            finalName = keyname[-1]
        for words, tags in s:
            value = value + " " + words
        removeWords = [' donated ', ' fundraising ', ' charity ', ' treatment ', 'awareness']
        if not any(word in value for word in removeWords):
            if "diagnosed with" in value:
                illnessValue = value.partition("diagnosed with")[2]
            elif "suffering from" in value:
                illnessValue = value.partition("suffering from")[2]
            elif "disease" in value:
                illnessValue = value.partition("disease")[0]
                illnessValue = illnessValue + "disease"
        if finalName.strip() is not '':
            if illnessValue.strip() is not '':
                illnessRelations.append([finalName,illnessValue])
    return illnessRelations

#---------------------------------------------------------------------------#
#----------------------------Template 7-------------------------------------#
#---------------------------------------------------------------------------#
#Financial_Status
def getPossessions(document):
    sentences = sent_tokenize(document)
    possessionRelations = []
    possessionSentences = []
    newList = []
    word = 'bought'
    wordlist = []
    wordlist.append(word)
    for synset in wordnet.synsets(word):
        if synset.name not in wordlist:
            for lemma in synset.lemmas():
                if lemma.name() not in wordlist:
                    wordlist.append(lemma.name())
    wordnet_lemmatizer = WordNetLemmatizer()
    if wordnet_lemmatizer.lemmatize(word) not in wordlist:
        wordlist.append(wordnet_lemmatizer.lemmatize(word))

    for value in wordlist:
        wordStructure = r'.*\b'+value+'\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                possessionSentences.append(sent)

    for i in range(len(possessionSentences)):
        newSent = pos_tag(word_tokenize(possessionSentences[i]))
        #print(newSent)
        #print("\n\n")
        newList.append(newSent)


    salaryFactor = r"""
                    FOUNDPOSSESSION: {<VBD|VB|NN><IN>?<DT><NNP|NN|JJ|NNS|IN|CD|DT|RB|\,|\$>*}
                    """
    cp = nltk.RegexpParser(salaryFactor)
    for s in newList:
        tree = cp.parse(s)
        for subtree in tree.subtrees():
            if subtree.label() == 'FOUNDPOSSESSION':
                treeExtract = subtree.pos()
                #print(treeExtract)
                value = ""
                nameList = []
                keyname = " "
                wordTagList = []
                for chunk in ne_chunk(s):
                    if hasattr(chunk, 'label'):
                        nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
                #print(nameList)
                for tag, word in nameList:
                    if tag == 'PERSON':
                        keyname = word
                for w, t in treeExtract:
                    wordTagList.append(w)
                for words, tags in wordTagList:
                    value = value + " " + words
                if keyname.strip() is not '':
                    possessionRelations.append([keyname,value])
    return possessionRelations

#---------------------------------------------------------------------------#
#----------------------------Template 8-------------------------------------#
#---------------------------------------------------------------------------#
#Recognition
def getTributes(document):
    sentences = sent_tokenize(document)
    tributeRelations = []
    tributeSentences = []
    newList = []
    word = r'.*\btribute\b.*\bto\b.*'
    for sent in sentences:
        if re.search(word, sent):
                tributeSentences.append(sent)
    for i in range(len(tributeSentences)):
        newSent = pos_tag(word_tokenize(tributeSentences[i]))
        newList.append(newSent)

    for s in newList:
        nameList = []
        keyname = []
        sentence = ''
        for chunk in ne_chunk(s):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        for tag, word in nameList:
            if tag == 'PERSON':
                keyname.append(word)
        finalName = keyname[0]
        for w, t in s:
            sentence = sentence + " " + w
        if finalName.strip() is not '':
            tributeRelations.append([finalName, sentence])
    #print(tributeRelations)
    return tributeRelations

#Recognition
def getAccolades(document):
    sentences = sent_tokenize(document)
    accoladeRelations = []
    accoladeSentences = []
    newList = []
    words = ['awarded', 'Honors', 'Awards', 'awards', 'honors']
    for value in words:
        wordStructure = r'.*\b'+value+'\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                accoladeSentences.append(sent)

    for i in range(len(accoladeSentences)):
        newSent = pos_tag(word_tokenize(accoladeSentences[i]))
        newList.append(newSent)
    for s in newList:
        yearStructure = r'.*\b\d{4}\b.*'
        nameList = []
        keyname = []
        year = ''
        finalName = ''
        award = ''
        for words, tags in s:
            if tags == 'CD':
                if re.search(yearStructure, words):
                    year = words
        for chunk in ne_chunk(s):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        for tag, word in nameList:
            if tag == 'PERSON':
                keyname.append(word)
        if keyname:
            finalName = keyname[0]
        for i in range(len(s)-1):
            if (s[i][0] == 'awarded') and (s[i+1][1] == 'DT'):
                for j in range(2,len(s)):
                    award = award + " " +s[j][0]
        if finalName.strip() is not '':
            if award.strip() is not '':
                accoladeRelations.append([finalName, year, award])
    return accoladeRelations
#---------------------------------------------------------------------------#
#----------------------------Template 9-------------------------------------#
#---------------------------------------------------------------------------#
#Philanthropic_Endeavors
def getPhilanthropicEndeavors(document):
    sentences = sent_tokenize(document)
    philanthropicRelations = []
    philanthropicSentences = []
    newList = []
    wordsList = ['gave', 'funded', 'charity']
    for value in wordsList:
        wordStructure = r'.*\b'+value+'\\b.*\$.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                philanthropicSentences.append(sent)
    addWords = ['donated']
    for value in addWords:
        wordStructure = r'.*\b'+value+'\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                philanthropicSentences.append(sent)

    for i in range(len(philanthropicSentences)):
        newSent = pos_tag(word_tokenize(philanthropicSentences[i]))
        newList.append(newSent)

    for s in newList:
        nameList = []
        keyname = []
        orgname = []
        keyPerson = ''
        amountDonated = ''
        for chunk in ne_chunk(s):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        for tag, word in nameList:
            if tag == 'PERSON':
                keyname.append(word)
            if tag == 'ORGANIZATION':
                orgname.append(word)
        #orgname = "[" + orgname + "]"
        for k in range(len(keyname)):
            if k == 0:
                keyPerson = keyname[0]
            elif k > 0:
                break
        amountFactor = r"""
                    FOUNDAMOUNT: {<\$><CD><CD>?}
                    """
        cp = nltk.RegexpParser(amountFactor)
        tree = cp.parse(s)
        wordTagList = []
        for subtree in tree.subtrees():
            treeExtract = []
            if subtree.label() == 'FOUNDAMOUNT':
                treeExtract = subtree.pos()
            for w, t in treeExtract:
                wordTagList.append(w)
        value = []
        for words, tags in wordTagList:
            value.append(words)
        if len(value) > 3:
            if value[2] == '$':
                amountDonated = value[0] + " " + value[1]
            else:
                amountDonated = value[0] + " " + value[1] + " " + value[2]
        if keyPerson.strip() is not '':
            if len(orgname) > 0:
                philanthropicRelations.append([keyPerson, orgname, amountDonated])
    return philanthropicRelations

#---------------------------------------------------------------------------#
#----------------------------Template 10------------------------------------#
#---------------------------------------------------------------------------#
#Death
def getDeathPlace(chunkedSentences):

    deathRelations = []
    deathPlace = re.compile(r'.*\bdied\b.*')

    for doc in chunkedSentences:
        for rel in nltk.sem.extract_rels('PER', 'GPE', doc, corpus = 'ace', pattern = deathPlace):
            if GeoText(rel['objtext']).cities:
                deathRelations.append([rel['subjtext'], rel['objtext']])
    return deathRelations

#Death
def getRestingPlace(chunkedSentences):

    restingRelations = []
    restingPlace = re.compile(r'.*\bburied\b.*')

    for doc in chunkedSentences:
        for rel in nltk.sem.extract_rels('PER','ORG', doc, corpus = 'ace', pattern=restingPlace):
            restingRelations.append([splitPOS(rel['subjtext']), splitPOS(rel['objtext'])])
    return restingRelations

#Death
def getDeathCause(document):
    sentences = sent_tokenize(document)

    deathCauseRelations = []
    diedSentences = []
    newList = []

    for sent in sentences:
        if re.search(r'.*\bdied\b.*', sent):
            diedSentences.append(sent)

    for i in range(len(diedSentences)):
        newSent = pos_tag(word_tokenize(diedSentences[i]))
        newList.append(newSent)

    deathCause = r"""
                DEATHCAUSE: {<NNP>+<VBD><IN><NN>*}
                """
    cp = nltk.RegexpParser(deathCause)
    for s in newList:
        tree = cp.parse(s)
        for subtree in tree.subtrees():
            if subtree.label() == 'DEATHCAUSE':
                reason = ""
                nameList = []
                for word, tag in s:
                    reason = reason + " " + word
                    if tag == 'NNP':
                        nameList.append(word)
                cause = reason.partition("died of")[2]
                deathReason = cause.partition(" at ")[0]
                if deathReason.strip():
                    deathCauseRelations.append([nameList[0],deathReason])
    return deathCauseRelations

#Death
def getDeathDate(chunkedSentences):
    deathDateRel = []

    date = r"""
    FOUND: {<NNP> <CD> <,> <CD>*}
      """
    cp = nltk.RegexpParser(date)

    for sent in chunkedSentences:
        if ' died/VBD' in str(sent) and 'PERSON' in str(sent):
            tree = cp.parse(sent)
            person = splitPOS((re.search(r"(PERSON.*)", str(sent)).group(0))[7:-1])
            noun_phrases_list = [' '.join(leaf[0] for leaf in tree.leaves()) for t in tree.subtrees()]
            date = re.search(r"(\d{1,2}) ([A-Za-z]+) (\d{4})", str(noun_phrases_list))
            if date:
                l = [person, date.group(0)]
                if l not in deathDateRel:
                    deathDateRel.append(l)
            else:
                date = re.search(r"([A-Za-z]+) (\d{1,2})\, (\d{4})", str(noun_phrases_list))
                if date:
                    l = [person, date.group(0)]
                    if l not in deathDateRel:
                        deathDateRel.append(l)
    return deathDateRel

#---------------------------------------------------------------------------#
#----------------------------Template 11------------------------------------#
#---------------------------------------------------------------------------#
#Publications
def getPublications(document):
    sentences = sent_tokenize(document)
    #publicationsRelations = []
    newList = []
    filmList = []
    bookList = []
    paperList = []
    filmWord = r'.*\bfilm\b.*'
    paperWord = r'.*\bpublished\b.*'
    bookWord = r'.*\bwritten\b.*'
    for i in range(len(sentences)):
        newSent = pos_tag(word_tokenize(sentences[i]))
        newList.append(newSent)
    for s in newList:
        sent = ''
        nameList = []
        for word, tag in s:
            sent = sent + " " + word
        for chunk in ne_chunk(s):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        for tag, word in nameList:
            if tag == 'PERSON':
                if re.search(filmWord, sent):
                    filmList.append(word)
                elif re.search(bookWord, sent):
                    bookList.append(word)
                elif re.search(paperWord, sent):
                    paperList.append(word)
    #publicationsRelations.append([bookList, paperList, filmList])
    #print(publicationsRelations)
    return bookList, paperList, filmList

#---------------------------------------------------------------------------#
#----------------------------Template 12------------------------------------#
#---------------------------------------------------------------------------#
#Innovations
def getInnovations(document):
    sentences = sent_tokenize(document)
    innovationRelations = []
    innovationSentences = []
    newList = []
    wordsList = ['cofounded', 'co-founded']
    yearSyntax = re.compile(r'\b\d{4}\b')
    for value in wordsList:
        wordStructure = r'.*\b'+value+'\\b.*'
        for sent in sentences:
            if re.search(wordStructure, sent):
                innovationSentences.append(sent)
    for i in range(len(innovationSentences)):
        newSent = pos_tag(word_tokenize(innovationSentences[i]))
        newList.append(newSent)
    for s in newList:
        nameList = []
        keyname = []
        orgname = []
        value = ''
        keyPerson = ''
        coFounder = ''
        cofoundedInnovation = ''
        yearInnovated = ''
        for word, tag in s:
            value = value + " " + word

        year = yearSyntax.findall(value)
        for y in range(len(year)):
            yearInnovated = year[0]
        for chunk in ne_chunk(s):
            if hasattr(chunk, 'label'):
                nameList.append((chunk.label(), ' '.join(c[0] for c in chunk)))
                #print(nameList)
        for tag, word in nameList:
            if tag == 'PERSON':
                keyname.append(word)

            if tag == 'ORGANIZATION':
                orgname.append(word)

        for k in range(len(keyname)):
            if k == 0:
                keyPerson = keyname[0]
            elif k == 1:
                coFounder = keyname[1]
            elif k > 1:
                break
        for o in range(len(orgname)):
            if o == 0:
                cofoundedInnovation = orgname[0]
            elif o > 0:
                break
        if cofoundedInnovation.strip() is not '':
            if not keyPerson == coFounder:
                innovationRelations.append([keyPerson, cofoundedInnovation, yearInnovated, coFounder])
    return innovationRelations

#--------------------------------------------------------------------------#
#---------------------------------MAIN-------------------------------------#
#--------------------------------------------------------------------------#
if __name__ == "__main__":

    # Read corpus
    with open('corpus/corpus.txt', 'r') as myfile:
        document = myfile.read()

    # Preprocess corpus
    sentences, tokens, posTaggedSentence, chunkedSentences = preprocess(document)

    #---------------------------------------------------------------------------#
    #----------------------------Template 1-------------------------------------#
    #---------------------------------------------------------------------------#
    template1 = Template('Key_People($key_person_name, $birth_place, $birth_date, $nationality)')

    t1 = []

    nationalityRelations = getNationality(document)
    birthDateRel = getBirthDate(posTaggedSentence)
    birthPlaceRel = getBirthPlace(chunkedSentences)

    for nat in nationalityRelations:
        t1.append([nat[0], ' ', ' ', nat[1]])

    for date in birthDateRel:
        found = False
        for t in t1:
            if t[0] == date[0]:
                t[1] = date[1]
                found = True
        if found == False:
            t1.append([date[0], date[1], ' ', ' '])

    for place in birthPlaceRel:
        found = False
        for t in t1:
            if t[0] == place[0]:
                t[2] = place[1]
                found = True
        if found == False:
            t1.append([place[0], ' ', place[1], ' '])

    print("--------------Template 1 - Key_People--------------")
    for template in t1:
        print(template1.substitute(key_person_name =  template[0], birth_place = template[1], birth_date = template[2], nationality = template[3]))
        print("\n")

    #---------------------------------------------------------------------------#
    #----------------------------Template 2-------------------------------------#
    #---------------------------------------------------------------------------#
    template2 = Template('Family($key_person_name, $ancestry, $spouse, $relatives, $father, $mother, $children)')

    t2 = []

    getAncestryRel = getAncestry(document)
    sentences, tokens, posTaggedSentence, chunkedSentences = preprocess(document)
    getSpouseRel = getSpouse(chunkedSentences)
    sentences, tokens, posTaggedSentence, chunkedSentences = preprocess(document)
    getRelativesRel = getRelatives(document)
    sentences, tokens, posTaggedSentence, chunkedSentences = preprocess(document)
    parentRelations = getParents(document)
    childRelations = getChildren(document)

    for a in getAncestryRel:
        t2.append([a[0], a[1], ' ', ' ', ' ', ' ', ' '])

    for a in getSpouseRel:
        found = False
        for t in t2:
            if t[0] == a[0]:
                t[2] = a[1]
                found = True
        if found == False:
            t2.append([a[0], ' ', a[1], ' ', ' ', ' ', ' '])

    for a in getRelativesRel:
        found = False
        for t in t2:
            if t[0] == a[0]:
                t[3] = a[1]
                found = True
        if found == False:
            t2.append([a[0], ' ', ' ', a[1], ' ', ' ', ' '])

    for a in parentRelations:
        found = False
        for t in t2:
            if t[0] == a[0]:
                t[4] = a[1]
                t[5] = a[2]
                found = True
        if found == False:
            t2.append([a[0], ' ', ' ', ' ', a[1], a[2], ' '])

    for a in childRelations:
        found = False
        for t in t2:
            if t[0] == a[0]:
                t[6] = a[1]
                found = True
        if found == False:
            t2.append([a[0], ' ', ' ', ' ', ' ', ' ', a[1]])

    print("--------------Template 2 - Family--------------")
    for template in t2:
        print(template2.substitute(key_person_name =  template[0], ancestry = template[1], spouse = template[2], relatives = template[3], father = template[4], mother = template[5], children = template[6]))
        print("\n")
    #---------------------------------------------------------------------------#
    #----------------------------Template 3-------------------------------------#
    #---------------------------------------------------------------------------#
    template3 = Template('Occupation($key_person_name, $work, $board_member_of)')

    t3 = []

    sentences, tokens, posTaggedSentence, chunkedSentences = preprocess(document)
    occRelations = getOccupation(chunkedSentences)
    boardRelations = getBoardMember(chunkedSentences)

    for occ in occRelations:
        t3.append([occ[0], occ[1], ' '])

    for board in boardRelations:
        found = False
        for t in t3:
            if t[0] == board[0]:
                t[2] = board[1]
                found = True
        if found == False:
            t3.append([board[0], board[1], ' '])

    print("--------------Template 3 - Occupation--------------")
    for template in t3:
        print(template3.substitute(key_person_name =  template[0], work = template[1],  board_member_of = template[2]))
        print("\n")

    #---------------------------------------------------------------------------#
    #----------------------------Template 4-------------------------------------#
    #---------------------------------------------------------------------------#
    template13 = Template('Education($key_person_name, $year, $degree, $discipline, $university)')

    t13 =[]

    educationRelations = getEducation(document)
    for rel in educationRelations:
        t13.append(template13.substitute(key_person_name =  rel[0], year = rel[1], degree = rel[2], discipline = rel[3], university = rel[4]))

    print("--------------Template 4 - Education--------------")
    for template in t13:
        print("\n" + template)

    #---------------------------------------------------------------------------#
    #----------------------------Template 5-------------------------------------#
    #---------------------------------------------------------------------------#
    template5 = Template('Career($key_person_name, $company, $title, $no_of_years)')

    sentences, tokens, posTaggedSentence, chunkedSentences = preprocess(document)
    careerRelations = getCareer(chunkedSentences)

    done = []
    print("--------------Template 5 - Career --------------")
    for template in careerRelations:
        if template not in done:
            print(template5.substitute(key_person_name =  template[0], company = template[1], title = template[2], no_of_years = template[3]))
            print("\n")
            done.append(template)

    #---------------------------------------------------------------------------#
    #----------------------------Template 6-------------------------------------#
    #---------------------------------------------------------------------------#
    template6 = Template('Health($key_person_name, $disability_flag, $disability, $illness)')

    t6 =[]

    illnessRelations = getIllnessRelations(document)
    disabilityRel = getDisability(document)
    for a in illnessRelations:
        found = False
        for b in disabilityRel:
            if a[0] == b[0]:
                t6.append([a[0], 'Y', ' ', a[1]])
                found = True
        if found == False:
            t6.append([a[0], 'N', ' ', a[1]])

    print("--------------Template 6 - Health --------------")
    for template in t6:
        print(template6.substitute(key_person_name =  template[0], disability_flag = template[1], disability = template[2], illness = template[3]))
        print("\n")

    #---------------------------------------------------------------------------#
    #----------------------------Template 7-------------------------------------#
    #---------------------------------------------------------------------------#
    template7 = Template('Financial_Status($key_person_name, $possessions)')
    t7 = []

    possessionRelations = getPossessions(document)
    for rel in possessionRelations:
        t7.append(template7.substitute(key_person_name =  rel[0], possessions = rel[1]))
    print("--------------Template 7 - Financial_Status --------------")
    for template in t7:
        print("\n" + template)

    #---------------------------------------------------------------------------#
    #----------------------------Template 8-------------------------------------#
    #---------------------------------------------------------------------------#
    template8 = Template('Recognition($key_person_name, $year, $accolade, $tribute)')

    t8 = []
    tributeRelations = getTributes(document)
    accoladeRelations = getAccolades(document)

    for a in accoladeRelations:
        t8.append([a[0], a[1], a[2], ' '])

    for a in tributeRelations:
        found = False
        for t in t8:
            if t[0] == a[0]:
                t[3] = a[1]
                found = True
        if found == False:
            t8.append([a[0], ' ', ' ', a[1]])

    print("--------------Template 8 - Recognition --------------")
    for template in t8:
        print(template8.substitute(key_person_name =  template[0], year = template[1], accolade = template[2], tribute = template[3]))
        print("\n")
    #---------------------------------------------------------------------------#
    #----------------------------Template 9-------------------------------------#
    #---------------------------------------------------------------------------#
    template9 = Template('Philanthropic_Endeavors($key_person_name, $charityOrganizations, $amount)')

    t9 = []

    philanthropicRelations = getPhilanthropicEndeavors(document)
    for rel in philanthropicRelations:
        t9.append(template9.substitute(key_person_name =  rel[0], charityOrganizations = rel[1], amount = rel[2]))
    print("--------------Template 9 - Philanthropic_Endeavors --------------")
    for template in t9:
        print("\n" + template)

    #---------------------------------------------------------------------------#
    #----------------------------Template 10------------------------------------#
    #---------------------------------------------------------------------------#
    template10 = Template('Death($key_person_name, $place_died, $date_died, $cause_of_death, $resting_place)')

    t10 = {}
    sentences, tokens, posTaggedSentence, chunkedSentences = preprocess(document)
    #----- Feature 1 - place_died
    deathPlaceRel = getDeathPlace(chunkedSentences)
    for rel in deathPlaceRel:
        t10[splitPOS(rel[0])] = {}
        t10[splitPOS(rel[0])]['place_died'] = splitPOS(rel[1])

    #----- Feature 2 - resting_place
    sentences, tokens, posTaggedSentence, chunkedSentences = preprocess(document)
    restingPlaceRel = getRestingPlace(chunkedSentences)
    for rel in restingPlaceRel:
        if rel[0] in t10:
            t10[rel[0]]['resting_place'] = rel[1]
        else:
            t10[rel[0]] = {}
            t10[rel[0]]['resting_place'] = rel[1]

    #----- Feature 2 - cause_of_death
    deathCauseRel = getDeathCause(document)
    for rel in deathCauseRel:
        if rel[0] in t10:
            t10[rel[0]]['cause_of_death'] = rel[1]
        else:
            t10[rel[0]] = {}
            t10[rel[0]]['cause_of_death'] = rel[1]

    #----- Feature 3 - death_date
    sentences, tokens, posTaggedSentence, chunkedSentences = preprocess(document)
    deathDateRel = getDeathDate(chunkedSentences)
    for rel in deathDateRel:
        if rel[0] in t10:
            t10[rel[0]]['date_died'] = rel[1]
        else:
            t10[rel[0]] = {}
            t10[rel[0]]['date_died'] = rel[1]

    print("--------------Template 10 - Death--------------")
    for key, value in t10.items():
        place = ' '
        date = ' '
        cause = ' '
        resting = ' '
        name = key
        for k, v in value.items():
            if 'place_died' in k:
                place = t10[key]['place_died']
            if 'date_died' in k:
                date = t10[key]['date_died']
            if 'cause_of_death' in k:
                cause = t10[key]['cause_of_death']
            if 'resting_place' in k:
                resting = t10[key]['resting_place']
        print(template10.substitute(key_person_name = name, place_died = place, date_died = date, cause_of_death = cause, resting_place = resting))
    print("\n")

    #---------------------------------------------------------------------------#
    #----------------------------Template 11------------------------------------#
    #---------------------------------------------------------------------------#
    template11 = Template('Publications($key_person_name, $books, $papers, $films)')

    t11 = []
    bookList, paperList, filmList = getPublications(document)

    for person in bookList:
        t11.append([person, 'Y', ' ', ' '])

    for person in paperList:
        found = False
        for t in t11:
            if person == t[0]:
                t[2] = 'Y'
                found = True
        if found == False:
            t11.append([person, ' ', 'Y', ' '])

    for person in filmList:
        found = False
        for t in t11:
            if person == t[0]:
                t[3] = 'Y'
                found = True
        if found == False:
            t11.append([person, ' ', ' ', 'Y'])

    print("--------------Template 11 - Publications--------------")
    for template in t11:
        print(template11.substitute(key_person_name =  template[0], books = template[1], papers = template[2], films = template[3]))
        print("\n")
    #---------------------------------------------------------------------------#
    #----------------------------Template 12------------------------------------#
    #---------------------------------------------------------------------------#
    template12 = Template('Innovations($key_person_name, $innovation, $year, $cofounder)')

    t12 = []
    innovationRelations = getInnovations(document)
    for rel in innovationRelations:
        t12.append(template12.substitute(key_person_name =  rel[0], innovation = rel[1], year = rel[2], cofounder = rel[3]))

    print("--------------Template 12 - Innovations--------------")
    for template in t12:
        print("\n" + template)
