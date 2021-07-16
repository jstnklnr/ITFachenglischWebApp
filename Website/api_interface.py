import requests
import json

class Api():
    def __init__(self, url:str):
        self.url = url

    def getUnits(self, book):
        res = requests.get(self.url + "/units?book=" + book, verify=False)

        unitList = []
        for item in json.loads(res.text):
            unitList.append(item['unit'])

        return unitList
    
    def getTopics(self):
        res = requests.get(self.url + "/topics", verify=False)

        topicList = []
        for item in json.loads(res.text):
            topicList.append(item['topic'])

        return topicList

    def getBooks(self):
        res = requests.get(self.url + "/books", verify=False)

        bookList = []
        for item in json.loads(res.text):
            bookList.append(item['book'])

        return bookList

    def getLanguages(self):
        res = requests.get(self.url + "/languages", verify=False)

        languageList = []
        for item in json.loads(res.text):
            languageList.append(item['book'])

        return languageList

    def getVocabulary(self, books:list, lang:str, amount=0, topics=[], units=[]):
        bookStr = ""
        idx = 0
        for item in books:
            bookStr += item
            
            if idx != len(books) - 1:
                bookStr += ","
            idx += 1
        
        request_string = ""
        if topics:
            topicStr = ""
            idx = 0
            for item in topics:
                topicStr += item
                if idx != len(topics) - 1:
                    topicStr += ","
                idx += 1

            request_string = self.url + "/vocabulary?book=" + bookStr + "&lang=" + lang + "&topics=" + topicStr
        else:
            unitStr = ""
            idx = 0
            for item in units:
                unitStr += item
                if idx != len(units) - 1:
                    unitStr += ","
                idx += 1

            request_string = self.url + "/vocabulary?book=" + bookStr + "&lang=" + lang + "&unit=" + unitStr 

        print(request_string)


        if amount != 0:
            request_string + "&amount=" + amount

        res = requests.get(request_string, verify=False)

        print(res.text)

        vocabularyList = []
        for item in json.loads(res.text):
            vocabularyList.append(item['unit'])

        return vocabularyList

print(Api("https://localhost:5000").getVocabulary(["IT Matters", "Mity Matters"], "English", topics=["Company", "Software"]))