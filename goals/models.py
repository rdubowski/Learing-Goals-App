from django.db import models


class LearningGoal(models.Model):
    name = models.CharField(blank=True, max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SingleTask(models.Model):
    text = models.CharField(blank=True, max_length=40)
    learninggoal = models.ForeignKey(LearningGoal, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:20]