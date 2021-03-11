import pytest
from goals.models import LearningGoal, SingleTask
from tests.factories import (
    LearningGoalFactory,
    SingleTaskFactory,
    UserFactory
)
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_client(django_user_model):
    """
    User fixture for tests with unprivileged user
    """
    example_user = UserFactory.build()
    created_user = django_user_model.objects.create_user(example_user)
    return created_user


def test_new_user(user_client):
    assert User.objects.count() == 1


def test_learning_goal_factory():
    learning_goal = LearningGoalFactory()
    single_lg_db = LearningGoal.objects.filter(name=learning_goal.name)
    assert single_lg_db.exists()


def test_multi_learning_goals():
    LearningGoalFactory()
    LearningGoalFactory()
    assert len(LearningGoal.objects.all()) == 2


def test_has_learning_goal_name():
    name = "My Goal"
    LearningGoalFactory(name=name)
    assert LearningGoal.objects.filter(name=name).exists()


def test_has_learning_goal_user(user_client):
    user = user_client
    LearningGoalFactory(user=user)
    assert LearningGoal.objects.filter(user=user).exists()


def test_learning_goal_str():
    learning_goal = LearningGoalFactory()
    from_db = LearningGoal.objects.get(name=learning_goal.name)
    assert str(from_db) == learning_goal.name


def test_task_factory():
    task = SingleTaskFactory()
    task_from_db = SingleTask.objects.get(text=task.text)
    assert task_from_db.completed is not None
    assert task_from_db.learninggoal is not None


def test_has_task_text():
    text = "My Task"
    SingleTaskFactory(text=text)
    task_from_db = SingleTask.objects.filter(text=text)
    assert task_from_db.exists()


def test_has_task_learning_goal():
    learning_goal = LearningGoalFactory()
    SingleTaskFactory(learninggoal=learning_goal)
    task_from_db = SingleTask.objects.filter(learninggoal=learning_goal)
    assert task_from_db.exists()


def test_task_str():
    text = "My Task"
    SingleTaskFactory(text=text)
    task_from_db = SingleTask.objects.get(text=text)
    assert str(task_from_db) == text


def test_task_not_completed():
    SingleTaskFactory()
    task_from_db = SingleTask.objects.get(pk=1)
    assert not task_from_db.completed

def test_task_ordering():
    learning_goal = LearningGoalFactory()
    task_1 = SingleTaskFactory(completed=True, learninggoal=learning_goal)
    task_2 = SingleTaskFactory(completed=False, learninggoal=learning_goal)
    task_3 = SingleTaskFactory(completed=True, learninggoal=learning_goal)
    learning_goals_tasks = LearningGoal.objects.get(
        name=learning_goal.name).tasks.all()
    assert list(learning_goals_tasks) == [task_1, task_3, task_2]