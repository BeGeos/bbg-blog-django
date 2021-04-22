from django.db import models
from ckeditor.fields import RichTextField


class Post(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    summary = models.CharField(max_length=512)
    post = RichTextField(blank=True, null=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_on = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=32)
    slug = models.SlugField(max_length=64)
    image = models.ImageField(upload_to="post_pics/", default="../staticfiles/images/default.jpg")

    def __str__(self):
        return self.title


class PostTag(models.Model):
    tag = models.CharField(max_length=24)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.tag

