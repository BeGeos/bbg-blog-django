from django.db import models
from ckeditor.fields import RichTextField


class News(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    summary = models.CharField(max_length=512)
    news = RichTextField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_on = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=32)
    slug = models.SlugField(max_length=64)
    image = models.ImageField(upload_to="news_pics/", default="default.jpg")

    def __str__(self):
        return self.title


class NewsTag(models.Model):
    tag = models.CharField(max_length=24)
    post_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.tag
