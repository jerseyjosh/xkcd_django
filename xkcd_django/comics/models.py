from django.db import models

class Comic(models.Model):
    """
    xkcd json response takes the form:
    {
        "month": "12",
        "num": 3026,
        "link": "",
        "year": "2024",
        "news": "",
        "safe_title": "Linear Sort",
        "transcript": "",
        "alt": "The best case is O(n), and the worst case is that someone checks why.",
        "img": "https://imgs.xkcd.com/comics/linear_sort.png",
        "title": "Linear Sort",
        "day": "18"
    }
    """
    comic_number = models.IntegerField(unique=True) # unique id for comic
    title = models.CharField(max_length=255) # title of comic
    alt_text = models.TextField() # alt text for comic
    transcript = models.TextField() # transcript of comic
    image_url = models.URLField() # url of comic
    publish_date = models.DateField() # publish date of comic
    embedding = models.JSONField(null=True, blank=True)  # Store embedding as JSON, defaults as null

    def __str__(self):
        return f"{self.comic_number}: {self.title}"