from flask import Flask
from flask_restful import reqparse
from flask_restful import Resource
import static

class Translation(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("word", type = str)
        self.reqparse.add_argument("lang", type = str)
        self.reqparse.add_argument("trans-lang", type = str)

    def get(self):
        db = static.database
        args = self.reqparse.parse_args()
        
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
                                    JOIN (SELECT vocabulary.translation FROM vocabulary JOIN languages ON languages.id = vocabulary.language 
                                    WHERE vocabulary.word = ? AND languages.language = ? LIMIT 1) AS t0 
                                    ON t0.translation = vocabulary.translation
                                    WHERE languages.language = ?
                                    """, tuple([args['word'], args["lang"], args["trans-lang"]]))
        return translations, 200