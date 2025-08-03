using System;

class Program
{
    static void Main()
    {
        using var manager = new NoteManager();

        // Add notes
        manager.AddNote("Call Client", "Follow up on feedback", "work");
        manager.AddNote("Grocery List", "Tomatoes, Rice, Spinach", "personal");

        // List all
        manager.ListNotes();

        // Filter by category
        manager.GetNotesByCategory("personal");

        // Delete the first note if it exists
        Console.WriteLine("\n🗑 Deleting First Note...");
        if (manager != null)
        {
            var firstNoteId = manager.GetFirstNoteId();
            if (!string.IsNullOrEmpty(firstNoteId))
                manager.DeleteNoteById(firstNoteId);
        }

        // List again
        manager.ListNotes();
    }
}
