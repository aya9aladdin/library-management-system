import logging as log
import json

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from config import DevelopmentConfig
from bson import json_util, ObjectId
from flask_cors import CORS

app = Flask(__name__)
config = DevelopmentConfig()
app.config.from_object(config)

CORS(app, resources={r"/*":{'origins':"*"}})

#DATABASE = "books_db"
COLLECTION = "books"

#MONGO_URI = f"mongodb://localhost:27017/{DATABASE}" 
client = MongoClient(app.config['MONGO_URI'])
db = client.get_default_database()  # This will use the configured database URI


api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='title is required')
parser.add_argument('ISBN', type=int, required=True, help='ISBN is required')
parser.add_argument('genre', type=str, required=True, help='genre is required')
parser.add_argument('author', type=str, required=True, help='author is required')
parser.add_argument('pub_year', type=int, required=True, help='pub_year is required')


class BooksRetrieval(Resource):
    def get(self):
        data = db[COLLECTION].find()

        books = json.loads(json_util.dumps(data))

        for book in books:
            book['_id'] = book['_id']['$oid']

        return books, 200

    def post(self):
        args = parser.parse_args()
        if db[COLLECTION].find_one({"ISBN": args.ISBN}):
            response = {
                "message": "Book with this ISBN already exists",
                "status_code": 409
            }
        else:
            db[COLLECTION].insert_one(args)
            response = {
                "message": "Book added successfully"
            }
        return response, 200

    
class BookModify(Resource):
    def get(self, book_id):
        try:
            obj_id = ObjectId(book_id)
        except Exception as e:
            return jsonify({"error": "Invalid ObjectId"}), 400

        book = db[COLLECTION].find_one({"_id": obj_id})
        if (not book):
            return 404, "invalid ID"
            
        book = json.loads(json_util.dumps(book))
        book["_id"] = book["_id"]["$"]
        return book, 200
    
    def put(self, book_id):
        args = parser.parse_args()
        data = db[COLLECTION].update_one(
        {"_id": ObjectId(book_id)},
        {"$set": args}
    )
        
        if data.matched_count == 0:
            return {"error": "Book not found"}, 404

        return {"message": "Book updated successfully"}, 200

    def delete(self, book_id):
        try:
            obj_id = ObjectId(book_id)
        except Exception as e:
            return jsonify({"error": "Invalid ObjectId"}), 400
        
        book = db[COLLECTION].find_one({"_id": obj_id})

        if (not book):
            return 404, "invalid ID"
            
        book = json.loads(json_util.dumps(book))
        book["_id"] = book["_id"]['$oid']
        db[COLLECTION].delete_one({"_id": obj_id})
        return book, 200

api.add_resource(BooksRetrieval, '/books/')
api.add_resource(BookModify, '/books/<string:book_id>')

if __name__ == '__main__':
    app.run(debug=True)
    
