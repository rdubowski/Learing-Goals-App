from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import SingleTask

from .models import Profile


def profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email
        )


def learning_goal_update_on_singletask(sender, instance, created, **kwargs):
        instance.learninggoal.save()

def learning_goal_delete_on_singletask(sender, instance, **kwargs):
        instance.learninggoal.save()
    

post_save.connect(profile, sender=User)
post_save.connect(learning_goal_update_on_singletask, sender=SingleTask)
post_delete.connect(learning_goal_delete_on_singletask, sender=SingleTask)
