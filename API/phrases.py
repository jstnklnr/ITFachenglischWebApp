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
        if not args['lang']:
            return {"Error": "Language is missing."}, 400   
        if not args['trans-lang']:
            return {"Error": "Translation language is missing."}, 400  

        #amount not acceptable
        if args["amount"] and args['amount'] < 1:
            return {"Error": "Amount is too low."}, 403
            
        limit_str = ""
        
        if args["amount"]:
            limit_str = "LIMIT ?"

        #SQL QUERYS
        phrases = db.query_dict(f"""
                                SELECT phrases.phrase, phrases.translation 
                                FROM phrases 
                                JOIN languages 
                                ON languages.id = phrases.language 
                                WHERE languages.language = ? 
                                ORDER BY random() {limit_str}
                                """, tuple([args['lang']] + ([args['amount']] if args["amount"] else [])))
        
        #SQL translation string
        trans_id_str = " OR ".join(["phrases.translation = ?"] * len(phrases))
        trans_id_list = []
        
        for item in phrases:
            trans_id_list.append(item['translation'])
        
        translations = db.query_dict(f"""
                                    SElECT phrases.phrase, phrases.translation 
                                    FROM phrases 
                                    JOIN languages 
                                    ON languages.id = phrases.language 
                                    WHERE languages.language = ? AND ({trans_id_str})
                                    """, tuple([args["trans-lang"]] + trans_id_list))

        
        print("AFTER SQL")
        
        for item in phrases:
            for translation in translations:
                if item["translation"] == translation["translation"]:
                    if not "translations" in item:
                        item["translations"] = []
                        
                    item["translations"].append(translation)   
        
        return phrases, 200
