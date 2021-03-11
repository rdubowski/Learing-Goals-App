from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import LearningGoal, SingleTask


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CreateGoalForm(forms.ModelForm):
    class Meta:
        model = LearningGoal
        fields = ["name"]


class SingleTaskForm(forms.ModelForm):
    class Meta:
        model = SingleTask
        fields = ["text"]
