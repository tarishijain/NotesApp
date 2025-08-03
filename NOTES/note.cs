using System;

public class Note
{
    public string Id { get; set; }
    public string Title { get; set; }
    public string Content { get; set; }
    public string Category { get; set; }
    public DateTime CreatedAt { get; set; }

    public Note(string title, string content, string category)
    {
        Id = Guid.NewGuid().ToString();
        Title = title;
        Content = content;
        Category = category.ToLower();
        CreatedAt = DateTime.Now;

        Console.WriteLine($"[Note Created] ID: {Id} Title: {Title}");
    }

    public override string ToString()
    {
        return $"[{Category.ToUpper()}] {Title} ({CreatedAt:yyyy-MM-dd HH:mm})\n{Content}\n---";
    }
}
