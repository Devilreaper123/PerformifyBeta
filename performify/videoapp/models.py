from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    artist_description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title
