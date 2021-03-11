from django.db.models.signals import post_delete, post_save

from .models import SingleTask


def learning_goal_update_on_singletask(sender, instance, created, **kwargs):
    instance.learninggoal.save()


def learning_goal_delete_on_singletask(sender, instance, **kwargs):
    instance.learninggoal.save()


post_save.connect(learning_goal_update_on_singletask, sender=SingleTask)
post_delete.connect(learning_goal_delete_on_singletask, sender=SingleTask)
