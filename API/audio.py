from flask import Flask
from flask_restful import reqparse
from flask_restful import Resource
import static

class Audio(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("amount", type = int)

    def get(self):
        db = static.database
        args = self.reqparse.parse_args()

        if args['amount'] and args['amount'] < 1:
            return {"Error": "Amount is to low."}, 403

        limit_str = ""
        
        if args["amount"]:
            limit_str = "LIMIT ?"

        result_list = db.query_dict(f"""
                                SELECT phrases.phrase
                                FROM phrases
                                ORDER BY random() {limit_str}
                                """, tuple([args['amount']] if args['amount'] else []))
        
        return result_list, 200
