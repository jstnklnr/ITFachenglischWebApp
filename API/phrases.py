from flask import Flask
from flask_restful import reqparse
from flask_restful import Resource
import static

class Phrases(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("lang", type = str)
        self.reqparse.add_argument("trans-lang", type = str)
        self.reqparse.add_argument("amount", type = int)

    def get(self):
        db = static.database
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
        phrases = db.query_dict(f"""
                                SELECT phrases.phrase, phrases.translation 
                                FROM phrases 
                                JOIN languages 
                                ON languages.id = phrases.language 
                                WHERE languages.language = ? 
                                ORDER BY random() LIMIT ?
                                """, tuple([args['lang'], args['amount']]))
        
        #SQL translation string
        trans_id_str = ""
        trans_id_list = []
        index = 0
        for item in phrases:
            trans_id_str += "translations.translation = ?"
            trans_id_list.append(item['translation'])
            index += 1
            
            if index != len(transDbList) - 1:
                trans_id_str += " OR "

        
        translations = db.query_dict(f"""
                                    SElECT phrases.phrase, phrases.translation 
                                    FROM phrases 
                                    JOIN languages 
                                    ON languages.id = phrases.language 
                                    WHERE languages.language = ? AND ({trans_id_str})
                                    """, tuple([args["trans-lang"]] + trans_id_list))

        
        for item in phrases:
            for translation in translations:
                if item["translation"] == translation["translation"]:
                    if item["translations"] is None:
                        item["translations"] = []
                        
                    item["translations"].append(translation)   
        
        return phrases, 200
