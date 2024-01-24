#! /usr/bin/env python3

import csv
import markdown

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
    'subjunction'
]
genderedCategories = [
    'noun',
    'determiner',
    'phrase'
]
otherCategories = [
    'link'
]
categories = nonGenderedCategories + genderedCategories + otherCategories

# creat an empty dictionary. This will contain a dictionary for each category that will have the list of things from the csv file
myWords = {}
for i in categories:
    myWords[i] = []

with open(wordListFile,newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        if line['kategorie'] in genderedCategories:
            myWords[line['kategorie']].append({'engelsk': line['engelsk'],
                                               'norsk': line['norsk'],
                                               'gender': line['gender']})
        elif line['kategorie'] in nonGenderedCategories:
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

for i in genderedCategories:
    nounText = ""
    # first nouns...
    for j in myWords[i]:
        nounText += "| [{}]({}) | {} | {} |\n".format(j['norsk'],"https://www.ordnett.no/search?language=no&phrase={}".format(j['norsk']),j['engelsk'],j['gender'])

    file = open ('headers/nounsHeader.md',mode='r')
    content = file.read()
    file.close()
    content = content.replace("<wordsGoHere>",nounText)
    outputFile = open('nouns.md','w')
    outputFile.write(content)
    # print("Updated: {}".format('headers/nounsHeader.md'))
    outputFile.close()

# now links
linkText = ""
# first nouns...
for i in myWords['link']:
    linkText += "| [{}]({}) | {} |\n".format(i['title'],i['link'],i['description'])

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
    html = html.replace("<table>","<center><table border=1>")
    html = html.replace("</table>","</table></center>")
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
