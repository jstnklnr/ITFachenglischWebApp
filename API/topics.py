from flask import Flask
from flask_restful import reqparse
from flask_restful import Resource
import static

class Topics(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument("book", type = str)

    def get(self):
        db = static.database
        args = self.reqparser.parse_args()
        
        books = []
        book_str = "1"
        
        if args['book']:
            books = args['book'].split(",")
            book_str = " OR ".join(["books.book = ?"] * len(books))
        
        return db.query_dict(f"""
                            SELECT topics.topic, t0.amount
                            FROM topics
                            JOIN (SELECT topics.id, COUNT(vocabulary.id) AS amount
                            FROM vocabulary JOIN topics ON topics.id = vocabulary.topic
                            JOIN books ON books.id = vocabulary.book
                            WHERE {book_str} GROUP BY topics.id) AS t0
                            ON t0.id = topics.id""", tuple(books)), 200