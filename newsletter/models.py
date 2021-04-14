from django.db import models


class Newsletter(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email

