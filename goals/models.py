from django.db import models


class Todo(models.Model):
    name = models.CharField(blank=True, max_length=40)
    text = models.CharField(max_length=40)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name