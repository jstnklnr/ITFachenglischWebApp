from flask import Flask
from flask import reqparse
from flask_restful import Resource

class Translation(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser
        reqparse.add_argument("word", type = str)
        reqparse.add_argument("languages", type = str)

    def get(self):
        args = reqparse.parse_args()
        
        if not args['word']:
            return {"Error": "Word is missing."}, 400
        if not args['lang']:
            return {"Error": "Language is missing."}, 400
            
        #SQL WHERE Languages
        langs = args['languages'].split(',')
        langsStr = ""
        langsList = []
        for i in range(langs):
            langsStr += "languages.language = ?"
            langsList.append(langs[i])

            if i != len(topics) - 1:
                langsStr += " OR "
       
        word = db.query_dict(f"""
                                    SELECT vocabulary.word 
                                    FROM vocabulary
                                    JOIN languages ON languages.id = vocabulary.language
                                    WHERE ({langsStr}) AND vocabulary.word = ?
                                    ORDER BY vocbulary.word
                                    """, tuple(langsStr + [args['word']]))
        return word, 200
