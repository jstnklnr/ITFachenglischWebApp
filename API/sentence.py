from flask import Flask
from flask import reqparse
from flask_restful import Resource

class Sentence(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("lang", type = str)
        self.reqparse.add_argument("trans-lang", type = str)
        self.reqparse.add_argument("amount", type = int)

    def get(self):
        args = self.reqparse.parse_args()

        #parameter missing
        if not args['amount']:
            return {"Error": "Amount is missing."}, 400
        if not args['lang']:
            return {"Error": "Language is missing."}, 400   
        if not args['trans-lang']:
            return {"Error": "Translation language is missing."}, 400  

        #amount not acceptable
        if args['amount'] > 100:
            return {"Error": "Amount is to high."}, 403
        if args['amount'] < 1:
            return {"Error": "Amount is to low."}, 403

        #SQL QUERYS
        resultList = None
        resultList = db.query_dict(f"""
                                SELECT phrases.phrase, #TODO________________________________________ 
                                FROM vocabulary
                                JOIN languages ON languages.id = vocabulary.language
                                JOIN books ON books.id = vocabulary.book
                                JOIN topics ON topics.id = vocabulary.topic
                                WHERE ({bookStr}) AND ({topicStr}) AND languages.language = 'English'
                                ORDER BY random() LIMIT ?
                                """, tuple(bookList + topicList + [args['amount']]))
        else:
            units = args['units'].split(',')  

            unitStr = ""
            unitList = []
            for i in range(units):
                unitStr += "books.book = ?"
                unitList.append(units[i])

                if i != len(units) - 1:
                    unitStr += " OR "

            resultList = db.query_dict(f"""
                                    SELECT vocabulary.word, vocabulary.translation 
                                    FROM vocabulary
                                    JOIN languages ON languages.id = vocabulary.language
                                    JOIN books ON books.id = vocabulary.book
                                    JOIN units ON units.id = vocabulary.unit
                                    WHERE ({unitStr}) AND languages.language = 'English' 
                                    ORDER BY random() LIMIT ?
                                    """, tuple(unitList + [args['amount']]))
        return resultList, 200
