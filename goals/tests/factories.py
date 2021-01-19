from django.contrib.auth.models import User
from goals.models import LearningGoal, SingleTask
import factory
from factory import Faker
import factory.fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    password = Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True)

    class Meta:
        model = User


class LearningGoalFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = LearningGoal


class SingleTaskFactory(factory.django.DjangoModelFactory):
    text = factory.fuzzy.FuzzyText()
    learninggoal = factory.SubFactory(LearningGoalFactory)

    class Meta:
        model = SingleTask

