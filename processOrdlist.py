#! /usr/bin/env python3

import csv

# file that we're going to work with...
wordListFile = 'ordlist.csv'

with open(wordListFile,newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        print("{}  {}  {}".format(line['kategorie'],line['norsk'],line['engelsk']))