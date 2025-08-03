# note_model.py
import uuid
import json
from datetime import datetime
from typing import List


class Note:
    def __init__(self, title: str, content: str, category: str, note_id=None, created_at=None):
        self.id = note_id if note_id else str(uuid.uuid4())
        self.title = title
        self.content = content
        self.category = category.lower()
        self.created_at = (
            datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            if created_at else datetime.now()
        )

    def __str__(self):
        return f"[{self.category.upper()}] {self.title} ({self.created_at.strftime('%Y-%m-%d %H:%M')})\n{self.content}\n---"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            content=data["content"],
            category=data["category"],
            note_id=data["id"],
            created_at=data["created_at"]
        )


class NoteManager:
    def __init__(self, filename=r"C:\Users\user\MyWorkspace\NOTES\notes.json"):
        self.notes: List[Note] = []
        self.filename = filename
        self.load_notes()

    def save_notes(self):
        with open(self.filename, "w") as f:
            json.dump([note.to_dict() for note in self.notes], f, indent=2)

    def load_notes(self):
        try:
            with open(self.filename, "r") as f:
                notes_data = json.load(f)
                self.notes = [Note.from_dict(data) for data in notes_data]
        except FileNotFoundError:
            self.notes = []

    def add_note(self, title: str, content: str, category: str):
        note = Note(title, content, category)
        self.notes.append(note)
        self.save_notes()
        return note

    def get_all_notes(self):
        return [note.to_dict() for note in self.notes]

    def get_notes_by_category(self, category: str):
        return [note.to_dict() for note in self.notes if note.category == category.lower()]

    def delete_note_by_id(self, note_id: str):
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                del self.notes[i]
                self.save_notes()
                return True
        return False
