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
        print(f"[Note Created] ID: {self.id} Title: {self.title}")

    def __del__(self):
        print(f"[Note Deleted] ID: {self.id} Title: {self.title}")

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
    def __init__(self, filename="NOTES\\notes.json"):
        self.notes: List[Note] = []
        self.filename = filename
        print("[NoteManager Initialized]")
        self.load_notes()

    def __del__(self):
        print("[NoteManager Destroyed] Cleaning up...")
        self.save_notes()

    def save_notes(self):
        with open(self.filename, "w") as f:
            json.dump([note.to_dict() for note in self.notes], f, indent=2)
        print("[Notes Saved]")

    def load_notes(self):
        try:
            with open(self.filename, "r") as f:
                notes_data = json.load(f)
                self.notes = [Note.from_dict(data) for data in notes_data]
            print("[Notes Loaded]")
        except FileNotFoundError:
            print("[No Existing Notes] Starting fresh.")

    def add_note(self, title: str, content: str, category: str):
        note = Note(title, content, category)
        self.notes.append(note)
        self.save_notes()
        print(f"[Note Added] {note.id}")

    def list_notes(self):
        print("\n📒 All Notes:")
        for note in self.notes:
            print(note)

    def get_notes_by_category(self, category: str):
        print(f"\n🔍 Notes in Category: {category.upper()}")
        for note in self.notes:
            if note.category == category.lower():
                print(note)

    def delete_note_by_id(self, note_id: str):
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                print(f"[Deleting Note] ID: {note.id}")
                del self.notes[i]
                self.save_notes()
                return
        print(f"[Not Found] No note with ID {note_id}")




if __name__ == "__main__":
    manager = NoteManager()

    # Add some notes
    manager.add_note("Call Client", "Follow up on feedback", "work")
    manager.add_note("Grocery List", "Tomatoes, Rice, Spinach", "personal")

    # List all
    manager.list_notes()

    # Filter by category
    manager.get_notes_by_category("personal")

    # Delete one by ID
    if manager.notes:
        manager.delete_note_by_id(manager.notes[0].id)

    # List again
    manager.list_notes()

    # Destructor will save on exit


