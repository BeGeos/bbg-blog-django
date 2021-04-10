from django.db import models


class News(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    summary = models.CharField(max_length=512)
    news = models.TextField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_on = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=32)
    slug = models.SlugField(max_length=64)

    def __str__(self):
        return self.title


class NewsImage(models.Model):
    post_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="news_pics")
    is_cover = models.BooleanField(default=False)


class NewsTag(models.Model):
    tag = models.CharField(max_length=24)
    post_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.tag
