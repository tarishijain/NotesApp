# app.py
from flask import Flask, jsonify, request
from note_model import NoteManager

app = Flask(__name__)
manager = NoteManager()


@app.route("/")
def index():
    return {"message": "Welcome to the Notes API!"}


@app.route("/notes", methods=["GET"])
def list_notes():
    return jsonify(manager.get_all_notes())


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    required = {"title", "content", "category"}
    if not data or not required.issubset(data.keys()):
        return jsonify({"error": "Missing fields"}), 400
    note = manager.add_note(data["title"], data["content"], data["category"])
    return jsonify(note.to_dict()), 201


@app.route("/notes/<category>", methods=["GET"])
def get_by_category(category):
    notes = manager.get_notes_by_category(category)
    return jsonify(notes)


@app.route("/notes/<note_id>", methods=["DELETE"])
def delete_note(note_id):
    success = manager.delete_note_by_id(note_id)
    if success:
        return jsonify({"message": "Note deleted"})
    return jsonify({"error": "Note not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
