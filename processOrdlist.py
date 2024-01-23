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
                                               'title': line['engelsk']})
        elif line['kategorie'] == 'other':
            myWords[line['kategorie']].append({'other': line['norsk']})
        # print("{}  {}  {}".format(line['kategorie'],line['norsk'],line['engelsk']))
print(myWords)