#! /usr/bin/env python3

import csv

# file that we're going to work with...
wordListFile = 'ordlist.csv'

# here are the categories that I've defined
categories = [
    'noun',
    'verb',
    'adjective',
    'adverb',
    'preposition',
    'determiner',
    'pronoun',
    'conjunction',
    'link',
    'other'
]

# creat an empty dictionary. This will contain a dictionary for each category that will have the list of things from the csv file
myWords = {}
for i in categories:
    myWords[i] = []



with open(wordListFile,newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        if line['kategorie'] == 'noun':
            myWords[line['kategorie']].append({'engelsk': line['engelsk'],
                                               'norsk': line['norsk'],
                                               'gender': line['gender']})
        elif line['kategorie'] in ['verb','adjective','adverb','perposition','determiner','pronoun','conjunction']:
            myWords[line['kategorie']].append({'engelsk': line['engelsk'],
                                               'norsk': line['norsk']})
        elif line['kategorie'] == 'link':
            myWords[line['kategorie']].append({'link': line['norsk'],
                                               'title': line['engelsk'],
                                               'description': line['gender']})
        elif line['kategorie'] == 'other':
            myWords[line['kategorie']].append({'other': line['norsk']})
        # print("{}  {}  {}".format(line['kategorie'],line['norsk'],line['engelsk']))

# now write a file for each type of word/thing...

nounText = ""
# first nouns...
for i in myWords['noun']:
    nounText += "| [{}]({}) | {} | {} |\n".format(i['norsk'],"https://www.ordnett.no/search?language=no&phrase={}".format(i['norsk']),i['engelsk'],i['gender'])

file = open ('headers/nounsHeader.md',mode='r')
content = file.read()
file.close()
content = content.replace("<wordsGoHere>",nounText)
outputFile = open('nouns.md','w')
outputFile.write(content)
outputFile.close()

# now links
linkText = ""
# first nouns...
for i in myWords['link']:
    linkText += "| [{}]({}) | {} |\n".format(i['link'],i['title'],i['description'])

file = open ('headers/linksHeader.md',mode='r')
content = file.read()
file.close()
content = content.replace("<wordsGoHere>",linkText)
outputFile = open('links.md','w')
outputFile.write(content)
outputFile.close()

similarCategories = [
    'verb',
    'adjective',
    'adverb',
    'preposition',
    'determiner',
    'pronoun',
    'conjunction'
]

for i in similarCategories:
    wordText = ""
    for j in myWords[i]:
        wordText += "| [{}]({}) | {} |\n".format(j['norsk'],"https://www.ordnett.no/search?language=no&phrase={}".format(j['norsk'].replace(" ","%20")),j['engelsk'])

    headerFilename = 'headers/' + i + 'sHeader.md'
    file = open (headerFilename,mode='r')
    content = file.read()
    file.close()
    content = content.replace("<wordsGoHere>",wordText)
    outputFilename = i + 's.md'
    outputFile = open(outputFilename,'w')
    outputFile.write(content)
    outputFile.close()
