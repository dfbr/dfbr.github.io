#! /usr/bin/env python3

import csv
import markdown
import simplejson
import json
import random
import html


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

# shuffle each one so that you don't always get them in the same order...
noOfWords = 0
for i in wordCategories:
    random.shuffle(myWords[i])
    noOfWords += len(myWords[i])
    # print("{} words in {}".format(len(myWords[i]), i))




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
    content = content.replace("<COUNT>",str(len(myWords[i])))
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
content = content.replace("<COUNT>",str(len(myWords['link'])))
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
    content = content.replace("<COUNT>",str(len(myWords[i])))
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

# print(jsonString)

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
# for word in words:
innerHTML += """
            <div id="norksOrd" class="carousel slide" data-bs-ride="carousel"></div>
        <script src="https://code.jquery.com/jquery-3.7.0.js"></script>
        <script>
            function shuffle(array)
            {
                let currentIndex = array.length, randomIndex;

                // While there remain elements to shuffle.
                while (currentIndex > 0) {

                    // Pick a remaining element.
                    randomIndex = Math.floor(Math.random() * currentIndex);
                    currentIndex--;

                    // And swap it with the current element.
                    [array[currentIndex], array[randomIndex]] = [
                        array[randomIndex], array[currentIndex]];
                }

                return array;
            }

            function updateText(data)
            
            {

                shuffle(data.words);
                setInterval(myFunction, delayInMilliseconds)
                for (let i = 0; i < data.words.length; i++) {
                    sleep(delayInMilliseconds).then(() =>
                    {
                        console.log(data.words[i].engelsk)
                        // set the elements to invisible
                        document.getElementById("engelsk").style.visibility = "hidden";
                        document.getElementById("category").style.visibility = "hidden";
                        document.getElementById("gender").style.visibility = "hidden";
                        // then update the text
                        document.getElementById("norsk").innerHTML = data.words[i].norsk
                        document.getElementById("engelsk").innerHTML = data.words[i].engelsk
                        document.getElementById("category").innerHTML = data.words[i].kategorie
                        document.getElementById("gender").innerHTML = data.words[i].gender

                        // then delay and set the answer to visible
                        sleep(delayInMilliseconds).then(() => 
                        {
                            document.getElementById("engelsk").style.visibility = "visible";
                            if (data.words[i].kategorie === "noun") {
                                document.getElementById("category").style.visibility = "visible";
                            }
                            document.getElementById("gender").style.visibility = "visible";

                        });
                    });
                }
            }

            var myWordsJson = "https://dfbr.github.io/words.json";
            var delayInMilliseconds = 1000; //2 seconds
            var myWords = [];
            $.getJSON(myWordsJson).done(function(data) { myWords = shuffle(data.words); });
            
            let carouselText = `
                <div class="carousel-inner">
                    <div class="carousel-item inactive" data-bs-interval="3000" id="question1" >
                        <h1 class="display-1 text-center" id="norsk">norsk1</h1>
                    </div>
                    <div class="carousel-item inactive" data-bs-interval="3000" id="answer1">
                        <h1 class="display-1 text-center" id="norskSvar">norskSvar1</h1>
                        <h1 class="display-6 text-center" id="engelsk">engelsk1</h1>
                        <h1 class="display-6 text-center" id="gender">gender1</h1>
                        <h1 class="display-6 text-center" id="category">category1</h1>
                    </div> 
                </div>`
            // shuffle(myWords);
            setTimeout(() => {
                let myText = "";
                for (let i = 0; i < myWords.length; i++)
                {
                    // console.log(myText)
                    let carouselItem = carouselText;
                    if (i === 0) { 
                        carouselItem = carouselItem.replace('<div class="carousel - item inactive" data-bs-interval="3000" id="question0" >', '<div class="carousel - item active" data-bs-interval="3000" id="question0" >');
                    }
                    carouselItem = carouselItem.replace("question1", "question" + i);
                    carouselItem = carouselItem.replace("answer1", "answer" + i);
                    carouselItem = carouselItem.replace("norsk1",myWords[i].norsk);
                    carouselItem = carouselItem.replace("norskSvar1", myWords[i].norsk);
                    carouselItem = carouselItem.replace("engelsk1", myWords[i].engelsk);
                    carouselItem = carouselItem.replace("gender1", myWords[i].gender);
                    carouselItem = carouselItem.replace("category1", myWords[i].kategorie);
                    myText += carouselItem;
                } 
                console.log(myText)
                document.getElementById("norksOrd").innerHTML = myText;
                document.getElementById("question0").setAttribute("class","carousel-item active");
            },1000)
            // window.alert("myText") 
            // document.getElementById("norksOrd").innerHTML = myText;
        </script>    
        </div>
            """
    # if word == words[0]:
    #     innerHTML = innerHTML.replace("carousel-item","carousel-item active")
    # innerHTML = innerHTML.replace("<NORSKWORD>",word['norsk'])
    # innerHTML = innerHTML.replace("<ENGELSKORD>",word['engelsk'])
    # innerHTML = innerHTML.replace("<GENDER>",word['gender'])
    # innerHTML = innerHTML.replace("<CATEGORY>",word['kategorie'])
outerhtml = outerhtml.replace("<INNERHTMLHERE>",innerHTML)
outerhtml = outerhtml.replace("<NOOFWORDS>",str(noOfWords))
html = headerhtml.replace("<BODYGOESHERE>",outerhtml)
# now write to a new file
outputFile = open(filename,'w')
outputFile.write(html)
# print("Updated: {}".format(outputFilename))
outputFile.close()