from django.db import models
from django.contrib.auth.models import User


class LearningGoal(models.Model):
    name = models.CharField(blank=True, max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SingleTask(models.Model):
    text = models.CharField(blank=True, max_length=40)
    learninggoal = models.ForeignKey(
        LearningGoal, on_delete=models.CASCADE, related_name="tasks"
    )
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-completed"]
