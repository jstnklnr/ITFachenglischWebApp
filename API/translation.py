from flask import Flask
from flask import reqparse
from flask_restful import Resource

class Translation(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser
        reqparse.add_argument("word", type = str)
        reqparse.add_argument("lang", type = str)
        reqparse.add_argument("trans-lang", type = str)

    def get(self):
        args = reqparse.parse_args()
        
        if not args['word']:
            return {"Error": "Word is missing."}, 400
        if not args['lang']:
            return {"Error": "Language is missing."}, 400
        if not args['lang']:
            return {"Error": "Translation language is missing."}, 400
       
        translations = db.query_dict(f"""
                                    SELECT vocabulary.word 
                                    FROM vocabulary
                                    JOIN languages ON languages.id = vocabulary.language
                                    WHERE lan AND vocabulary.word = ?
                                    ORDER BY vocbulary.word
                                    """, tuple(langsStr + [args['word']]))
        return word, 200