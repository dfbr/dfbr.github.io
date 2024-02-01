#! /usr/bin/env python3

import csv
import markdown
import simplejson
import json
import random


# file that we're going to work with...
wordListFile = 'ordlist.csv'

# here are the categories that I've defined
nonGenderedCategories = [
    'verb',
    'adjective',
    'adverb',
    'preposition',
    'pronoun',
    'conjunction',
    'subjunction',
    'phrase'
]
genderedCategories = [
    'noun',
    'determiner'
]
otherCategories = [
    'link'
]
wordCategories = nonGenderedCategories + genderedCategories
categories = nonGenderedCategories + genderedCategories + otherCategories

# creat an empty dictionary. This will contain a dictionary for each category that will have the list of things from the csv file
myWords = {}
for i in categories:
    myWords[i] = []

with open(wordListFile,newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        myWords[line['kategorie']].append({'engelsk': line['engelsk'],
                                          'norsk': line['norsk'],
                                          'gender': line['gender']})

# now write a file for each type of word/thing...
for i in genderedCategories:
    nounText = ""
    # first nouns...
    for j in myWords[i]:
        nounText += "| [{}]({}) | {} | {} |\n".format(j['norsk'],"https://www.ordnett.no/search?language=no&phrase={}".format(j['norsk']),j['engelsk'],j['gender'])

    filename = 'headers/' + i + 'sHeader.md'
    file = open (filename,mode='r')
    content = file.read()
    file.close()
    content = content.replace("<wordsGoHere>",nounText)
    outputFilename = i + 's.md'
    outputFile = open(outputFilename,'w')
    outputFile.write(content)
    # print("Updated: {}".format('headers/nounsHeader.md'))
    outputFile.close()

# now links
linkText = ""
# first nouns...
for i in myWords['link']:
    linkText += "| [{}]({}) | {} |\n".format(i['norsk'],i['engelsk'],i['gender'])

file = open ('headers/linksHeader.md',mode='r')
content = file.read()
file.close()
content = content.replace("<wordsGoHere>",linkText)
outputFile = open('links.md','w')
outputFile.write(content)
# print("Updated: {}".format('headers/linksHeader.md'))
outputFile.close()


for i in nonGenderedCategories:
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
    # print("Updated: {}".format(outputFilename))
    outputFile.close()

# now convert files to html using markdown...
for i in categories:
    filename = i + "s.md"
    headerHTMLFile = 'headers/htmlHeader.html'
    outerhtml = open(headerHTMLFile,'r').read()
    readingFile = open(filename,'r')
    content = readingFile.read()
    html = markdown.markdown(content, extensions=['tables'])
    html = html.replace(".md\"",".html\"")
    html = html.replace("<table>","<table class=\"table table-striped table-bordered\"")
    html = html.replace("</table>","</table>")
    outerhtml = outerhtml.replace("<BODYGOESHERE>",html)
    # now write to a new file
    outputFilename = i + "s.html" 
    outputFile = open(outputFilename,'w')
    outputFile.write(outerhtml)
    # print("Updated: {}".format(outputFilename))
    outputFile.close()

# now the same but for README.md -> index.html
filename = "README.md"
readingFile = open(filename,'r')
content = readingFile.read()
headerHTMLFile = 'headers/htmlHeader.html'
outerhtml = open(headerHTMLFile,'r').read()
html = markdown.markdown(content, extensions=['tables'])
html = html.replace(".md\"",".html\"")
html = html.replace("<table>","<center><table border=1>")
html = html.replace("</table>","</table></center>")
outerhtml = outerhtml.replace("<BODYGOESHERE>",html)
# now write to a new file
outputFilename = "index.html"
outputFile = open(outputFilename,'w')
outputFile.write(outerhtml)
# print("Updated: {}".format(outputFilename))
outputFile.close()

# now create a json of all the words only...
outputFilename = 'words.json'
jsonString = '{ "words": ['
for i in wordCategories:
    for j in myWords[i]:
        jsonString += "{"
        jsonString += '"kategorie": "{}",'.format(i)
        jsonString += '"norsk": "{}",'.format(j['norsk'])
        jsonString += '"engelsk": "{}",'.format(j['engelsk'])
        jsonString += '"gender": "{}"'.format(j['gender'])
        jsonString += "},"
jsonString = jsonString[:-1] # remove the last comma
jsonString += "]}"

print(jsonString)
with open(outputFilename, "w") as outputFile:
    # magic happens here to make it pretty-printed
    outputFile.write(
        simplejson.dumps(simplejson.loads(jsonString), indent=4, sort_keys=True)
    )
filename = "carousel.html"
headerHTMLFile = 'headers/htmlHeader.html'
headerhtml = open(headerHTMLFile,'r').read()
readingFile = open(filename,'r')
content = readingFile.read()
outerhtml = """
        <div id="norksOrd" class="carousel slide" data-bs-ride="carousel">
            <INNERHTMLHERE>
        </div>
"""
innerHTML = ""

words = json.loads(jsonString)['words']
random.shuffle(words)
for word in words:
    innerHTML += """
            <div class="carousel-inner">
                <div class="carousel-item" data-bs-interval="3000">
                    <h1 class="display-1 text-center" id="norsk"><NORSKWORD></h1>
                </div>
                <div class="carousel-item" data-bs-interval="3000">
                    <h1 class="display-1 text-center" id="norsk"><NORSKWORD></h1>
                    <h1 class="display-6 text-center" id="engelsk"><ENGELSKORD></h1>
                    <h1 class="display-6 text-center" id="gender"><GENDER></h1>
                    <h1 class="display-6 text-center" id="category"><CATEGORY></h1>
                </div>
            </div>
            """
    if word == words[0]:
        innerHTML = innerHTML.replace("carousel-item","carousel-item active")
    innerHTML = innerHTML.replace("<NORSKWORD>",word['norsk'])
    innerHTML = innerHTML.replace("<ENGELSKORD>",word['engelsk'])
    innerHTML = innerHTML.replace("<GENDER>",word['gender'])
    innerHTML = innerHTML.replace("<CATEGORY>",word['kategorie'])
outerhtml = outerhtml.replace("<INNERHTMLHERE>",innerHTML)
html = headerhtml.replace("<BODYGOESHERE>",outerhtml)
# now write to a new file
outputFile = open(filename,'w')
outputFile.write(html)
# print("Updated: {}".format(outputFilename))
outputFile.close()