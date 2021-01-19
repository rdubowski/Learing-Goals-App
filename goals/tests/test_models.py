import datetime
import pytest
from goals.tests.test import TestCase
from goals.models import Profile, LearningGoal, SingleTask
from goals.tests.factories import LearningGoalFactory, SingleTaskFactory

class TestUser(TestCase):
    def test_create_profile(self):
        '''A new user has automatically profile created'''
        user = self.make_user()
        assert Profile.objects.filter(user=user).exists()


class TestLearningGoal(TestCase):
    def test_learing_goal_factory(self):
        learning_goal = LearningGoalFactory()
        assert learning_goal is not None
        assert learning_goal.name != ""
        assert learning_goal.user is not None

    def test_has_learning_goal_name(self):
        name = "My Goal"
        learning_goal = LearningGoalFactory(name=name)
        assert learning_goal.name == name


    def test_has_learning_goal_user(self):
        user = self.make_user()
        learning_goal = LearningGoalFactory(user=user)
        assert learning_goal.user == user

    def test_learning_goal_str(self):
        learning_goal = LearningGoalFactory()
        assert str(learning_goal) == learning_goal.name
    

class TestSingleTask(TestCase):
    def test_task_factory(self):
        task = SingleTaskFactory()
        assert task.completed is not None
        assert task.text != ""
        assert task.learninggoal is not None

    def test_has_task_text(self):
        text = "My Task"
        task = SingleTaskFactory(text=text)
        assert task.text == text

    def test_has_task_learning_goal(self):
        learning_goal = LearningGoalFactory()
        task = SingleTaskFactory(learninggoal=learning_goal)
        assert task.learninggoal == learning_goal

    def test_task_str(self):
        task = SingleTaskFactory()
        assert str(task) == task.text
    
    def test_task_ordering(self):
        learning_goal = LearningGoalFactory()
        task_1 = SingleTaskFactory(completed=False, learninggoal=learning_goal)
        task_2 = SingleTaskFactory(completed=True, learninggoal=learning_goal)
        task_3 = SingleTaskFactory(completed=False, learninggoal=learning_goal)
        learning_goals_tasks = LearningGoal.objects.get(name=learning_goal.name).tasks.all()
        assert list(learning_goals_tasks) == [task_1, task_3, task_2]


