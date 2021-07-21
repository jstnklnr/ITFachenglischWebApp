from flask import Flask
from flask_restful import reqparse
from flask_restful import Resource
import static

class Audio(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("lang", type = str)
        self.reqparse.add_argument("amount", type = int)

    def get(self):
        db = static.database
        args = self.reqparse.parse_args()

        if not args["lang"]:
            return {"Error": "No language given."}, 400

        if args['amount'] and args['amount'] < 1:
            return {"Error": "Amount is too low."}, 403

        langs = args['lang'].split(',')
        langs_str = " OR ".join(["languages.language = ?"] * len(langs))

        limit_str = ""
        
        if args["amount"]:
            limit_str = "LIMIT ?"

        result_list = db.query_dict(f"""
                                SELECT phrases.phrase, phrases.audio
                                FROM phrases 
                                JOIN languages 
                                ON languages.id = phrases.language 
                                WHERE {langs_str}
                                ORDER BY random() {limit_str}
                                """, tuple(langs + ([args['amount']] if args['amount'] else [])))
        
        return result_list, 200
