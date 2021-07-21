import requests
import json

class Api():
    def __init__(self, url:str):
        self.url = url

    def getUnits(self, book):
        res = requests.get(self.url + "/units?book=" + book, verify=False)

        unitList = []
        for item in json.loads(res.text):
            unitList.append(item)

        return unitList
    
    def getTopics(self):
        res = requests.get(self.url + "/topics", verify=False)

        topicList = []
        for item in json.loads(res.text):
            topicList.append(item)

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
            languageList.append(item['language'])

        return languageList

    def getVocabulary(self, book:list, lang:str, amount=0, topic=[], unit=[]):
        bookStr = ""
        idx = 0
        for item in book:
            bookStr += item
            
            if idx != len(book) - 1:
                bookStr += ","
            idx += 1
        
        request_string = ""
        if topic:
            topicStr = ""
            idx = 0
            for item in topic:
                topicStr += item
                if idx != len(topic) - 1:
                    topicStr += ","
                idx += 1

            request_string = self.url + "/vocabulary?book=" + bookStr + "&lang=" + lang + "&topic=" + topicStr
        else:
            unitStr = ""
            idx = 0
            for item in unit:
                unitStr += item
                if idx != len(unit) - 1:
                    unitStr += ","
                idx += 1

            request_string = self.url + "/vocabulary?book=" + bookStr + "&lang=" + lang + "&unit=" + unitStr 

        if amount != 0:
            request_string += "&amount=" + amount

        res = requests.get(request_string, verify=False)

        vocabularyList = []
        for item in json.loads(res.text):
            vocabularyList.append({"word": item['word'], "language": item['language']})

        return vocabularyList

    def getTranslation(self, word:str, lang:str, trans_lang:str):
        res = requests.get(self.url + "/translation?word=" + word + "&lang=" + lang + "&trans-lang=" + trans_lang, verify=False)

        transList = []
        for item in json.loads(res.text):
            transList.append(item['word'])

        return transList

    def getAudio(self, lang:str, amount:int):
        res = requests.get(self.url + "/audio?lang=" + lang + "&amount=" + amount, verify=False)

        audioList = []
        for item in json.loads(res.text):
            audioList.append({"phrase": item['phrase'], "audio": item['audio']})

        return audioList

    def get_phrases_amount(self):
        res = requests.get(self.url + "/phrases?get-amount=true", verify=False)
        amount = json.loads(res.text)['amount']

        return amount 

#print(Api("https://localhost:5000").getTranslation("für etwas Werbung machen", "German", "English"))