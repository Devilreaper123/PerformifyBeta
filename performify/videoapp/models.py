from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.CharField(max_length=500)  # Large enough to handle multiple tags
    artist_description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title
