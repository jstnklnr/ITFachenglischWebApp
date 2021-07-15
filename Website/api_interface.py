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

print(Api("https://localhost:5000").getBooks())