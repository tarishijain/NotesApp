using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

public class NoteManager : IDisposable
{
    private List<Note> notes;
    private string filename;

    public NoteManager(string filename = "notes.json")
    {
        this.filename = filename;
        notes = new List<Note>();
        Console.WriteLine("[NoteManager Initialized]");
        LoadNotes();
    }

    public void Dispose()
    {
        Console.WriteLine("[NoteManager Destroyed] Cleaning up...");
        SaveNotes();
    }

    public void AddNote(string title, string content, string category)
    {
        var note = new Note(title, content, category);
        notes.Add(note);
        SaveNotes();
        Console.WriteLine($"[Note Added] {note.Id}");
    }

    public void ListNotes()
    {
        Console.WriteLine("\n📒 All Notes:");
        foreach (var note in notes)
        {
            Console.WriteLine(note);
        }
    }

    public void GetNotesByCategory(string category)
    {
        Console.WriteLine($"\n🔍 Notes in Category: {category.ToUpper()}");
        foreach (var note in notes)
        {
            if (note.Category == category.ToLower())
            {
                Console.WriteLine(note);
            }
        }
    }

    public void DeleteNoteById(string noteId)
    {
        var note = notes.Find(n => n.Id == noteId);
        if (note != null)
        {
            Console.WriteLine($"[Deleting Note] ID: {note.Id}");
            notes.Remove(note);
            SaveNotes();
        }
        else
        {
            Console.WriteLine($"[Not Found] No note with ID {noteId}");
        }
    }

    private void SaveNotes()
    {
        var json = JsonSerializer.Serialize(notes, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(filename, json);
        Console.WriteLine("[Notes Saved]");
    }

    private void LoadNotes()
    {
        if (!File.Exists(filename))
        {
            Console.WriteLine("[No Existing Notes] Starting fresh.");
            return;
        }

        var json = File.ReadAllText(filename);
        notes = JsonSerializer.Deserialize<List<Note>>(json) ?? new List<Note>();
        Console.WriteLine("[Notes Loaded]");
    }
}
