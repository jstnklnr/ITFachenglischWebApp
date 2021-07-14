from flask import Flask
from flask import reqparse
from flask_restful import Resource

class Phrase(Resource):
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
        transDbList = db.query_dict(f"""
                                SELECT phrases.translation,
                                FROM phrases
                                ORDER BY random() LIMIT ?
                                """, tuple(args['lang'] + args['amount']))
        
        #SQL translation string
        transIdStr = ""
        transIdList = []
        idx = 0
        for item in transDbList:
            transIdStr += "translations.translation = ?"
            transIdList.append(item['translation'])
            idx += 1
            
            if idx != len(transDbList) - 1:
                transIdStr += " OR "
#############################################################################
        phraseList = db.query_dict(f"""
                                SELECT phrases.phrase,
                                FROM phrases
                                JOIN languages ON languages.id = phrases.language
                                WHERE languages.language = ? AND ({transIdStr})
                                ORDER BY random()
                                """, tuple([args['lang']] + transIdList))
        
        translationList = db.query_dict(f"""
                                SELECT phrases.phrase,
                                FROM phrases
                                JOIN languages ON languages.id = phrases.language
                                WHERE languages.language = ? AND ({transIdStr})
                                ORDER BY random()
                                """, tuple([args['trans-lang']] + transIdList))
        
        resultList = []
        for item in phraseList:
            
        
        return resultList, 200
