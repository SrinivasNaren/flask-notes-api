# app.py

from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# In-memory database (list of notes)
notes = []

# Parser to handle incoming data
parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help="Title cannot be blank!")
parser.add_argument('content', type=str, required=True, help="Content cannot be blank!")

class Note(Resource):
    def get(self):
        return {"notes": notes}, 200

    def post(self):
        args = parser.parse_args()
        note = {
            "id": len(notes) + 1,
            "title": args['title'],
            "content": args['content']
        }
        notes.append(note)
        return note, 201

    def put(self):
        args = parser.parse_args()
        for note in notes:
            if note['title'] == args['title']:
                note['content'] = args['content']
                return note, 200
        return {"message": "Note not found"}, 404

    def delete(self):
        args = parser.parse_args()
        global notes
        notes = [note for note in notes if note['title'] != args['title']]
        return {"message": "Note deleted if it existed."}, 200

# Adding URL endpoint
api.add_resource(Note, '/notes')

if __name__ == '__main__':
    app.run(debug=True)
