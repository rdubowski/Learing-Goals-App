import pytest
from goals.models import Profile, LearningGoal, SingleTask
from goals.tests.factories import (
    LearningGoalFactory,
    SingleTaskFactory,
    UserFactory
)
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db

import pytest


@pytest.fixture
def user_client(django_user_model):
    """
    User fixture for tests with unprivileged user
    """
    example_user = UserFactory.build()
    created_user = django_user_model.objects.create_user(example_user)
    return created_user


@pytest.mark.django_db
def test_new_user(user_client):
    assert User.objects.count() == 1



@pytest.mark.django_db
def test_learing_goal_factory():
    learning_goal = LearningGoalFactory()
    assert learning_goal is not None
    assert learning_goal.name != ""
    assert learning_goal.user is not None


def test_has_learning_goal_name():
    name = "My Goal"
    learning_goal = LearningGoalFactory(name=name)
    assert learning_goal.name == name


def test_has_learning_goal_user(user_client):
    user = user_client
    learning_goal = LearningGoalFactory(user=user)
    assert learning_goal.user == user


def test_learning_goal_str():
    learning_goal = LearningGoalFactory()
    assert str(learning_goal) == learning_goal.name


def test_task_factory():
    task = SingleTaskFactory()
    assert task.completed is not None
    assert task.text != ""
    assert task.learninggoal is not None


def test_has_task_text():
    text = "My Task"
    task = SingleTaskFactory(text=text)
    assert task.text == text


def test_has_task_learning_goal():
    learning_goal = LearningGoalFactory()
    task = SingleTaskFactory(learninggoal=learning_goal)
    assert task.learninggoal == learning_goal


def test_task_str():
    task = SingleTaskFactory()
    assert str(task) == task.text


def test_task_ordering():
    learning_goal = LearningGoalFactory()
    task_1 = SingleTaskFactory(completed=False, learninggoal=learning_goal)
    task_2 = SingleTaskFactory(completed=True, learninggoal=learning_goal)
    task_3 = SingleTaskFactory(completed=False, learninggoal=learning_goal)
    learning_goals_tasks = LearningGoal.objects.get(
        name=learning_goal.name).tasks.all()
    assert list(learning_goals_tasks) == [task_1, task_3, task_2]