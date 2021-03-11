import pytest
from django.urls import reverse
from goals.models import LearningGoal, SingleTask
from tests.factories import UserFactory, LearningGoalFactory, SingleTaskFactory


pytestmark = pytest.mark.django_db


def test_welcome_page_view_unauth(client):
    url = reverse("welcome_screen")
    resp = client.get(url)
    assert resp.status_code == 200
    assert "This is a simple app to manage your tasks." in str(resp.content)


def test_welcome_page_view_auth(client):
    user = UserFactory()
    url = reverse("welcome_screen")
    client.force_login(user)
    resp = client.get(url)
    assert resp.status_code == 302


def test_dashboard_view_auth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    single_task = SingleTaskFactory(learninggoal=learning_goal)
    url = reverse("dashboard")
    client.force_login(user)
    resp = client.get(url)
    assert resp.status_code == 200
    assert learning_goal.name in str(resp.content)
    assert single_task.text in str(resp.content)


def test_dashboard_view_unauth(client):
    url = reverse("dashboard")
    resp = client.get(url)
    assert resp.status_code == 302


def test_dashboard_table_view_auth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    url = reverse("dashboard_table")
    client.force_login(user)
    resp = client.get(url)
    assert resp.status_code == 200
    assert learning_goal.name in str(resp.content)


def test_dashboard_table_view_unauth(client):
    url = reverse("dashboard_table")
    resp = client.get(url)
    assert resp.status_code == 302


def test_create_goal_view_auth_get(client):
    user = UserFactory()
    url = reverse("create_goal")
    client.force_login(user)
    resp = client.get(url)
    assert resp.status_code == 200


def test_create_goal_view_auth_post(client):
    user = UserFactory()
    url = reverse("create_goal")
    client.force_login(user)
    resp = client.post(url, data={"name": "learnname"})
    assert resp.status_code == 302
    assert LearningGoal.objects.get(pk=1).name == "learnname"


def test_create_goal_view_unauth_post(client):
    url = reverse("create_goal")
    resp = client.post(url, data={"name": "learnname"})
    assert resp.status_code == 302
    assert LearningGoal.objects.count() == 0


def test_delete_goal_view_auth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    client.force_login(user)
    url = reverse("delete_goal", kwargs={"pk": learning_goal.pk})
    resp = client.post(url)
    assert resp.status_code == 302
    assert LearningGoal.objects.count() == 0


def test_delete_goal_view_unauth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    url = reverse("delete_goal", kwargs={"pk": learning_goal.pk})
    resp = client.post(url)
    assert resp.status_code == 302
    assert LearningGoal.objects.count() == 1


def test_change_goal_name_view_get_auth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    client.force_login(user)
    url = reverse("change_goal_name", kwargs={"pk": learning_goal.pk})
    resp = client.get(url)
    assert resp.status_code == 200
    assert learning_goal.name in str(resp.content)


def test_change_goal_name_view_post_auth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    client.force_login(user)
    url = reverse("change_goal_name", kwargs={"pk": learning_goal.pk})
    resp = client.post(url, data={"name": "learnname"})
    assert resp.status_code == 302
    assert LearningGoal.objects.get(pk=1).name == "learnname"


def test_change_goal_name_view_post_unauth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    url = reverse("change_goal_name", kwargs={"pk": learning_goal.pk})
    resp = client.post(url, data={"name": "learnname"})
    assert resp.status_code == 302
    assert LearningGoal.objects.get(pk=1).name == learning_goal.name


def test_tasks_list_view_auth_get(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    single_task_1 = SingleTaskFactory(learninggoal=learning_goal)
    single_task_2 = SingleTaskFactory(learninggoal=learning_goal)
    single_task_3 = SingleTaskFactory(learninggoal=learning_goal)
    url = reverse("task_list_url", kwargs={"pk": learning_goal.pk})
    client.force_login(user)
    resp = client.get(url)
    assert resp.status_code == 200
    assert learning_goal.name in str(resp.content)
    assert single_task_1.text in str(resp.content)
    assert single_task_2.text in str(resp.content)
    assert single_task_3.text in str(resp.content)


def test_tasks_list_view_auth_post(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    url = reverse("task_list_url", kwargs={"pk": learning_goal.pk})
    client.force_login(user)
    resp = client.post(url, data={"name": "testtask123"})
    assert resp.status_code == 200
    assert SingleTask.objects.count() == 1
    assert not SingleTask.objects.get(pk=1).completed


def test_tasks_list_view_unauth_get(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    url = reverse("task_list_url", kwargs={"pk": learning_goal.pk})
    resp = client.get(url)
    assert resp.status_code == 302
    assert SingleTask.objects.count() == 0


def test_tasks_list_view_unauth_post(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    url = reverse("task_list_url", kwargs={"pk": learning_goal.pk})
    resp = client.post(url, data={"name": "testtask123"})
    assert resp.status_code == 302


def test_task_complete_view_auth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    single_task = SingleTaskFactory(learninggoal=learning_goal)
    url = reverse("task_complete_url", kwargs={"id": single_task.pk})
    client.force_login(user)
    resp = client.post(url)
    assert resp.status_code == 200
    assert SingleTask.objects.get(pk=single_task.pk).completed


def test_task_complete_view_unauth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    single_task = SingleTaskFactory(learninggoal=learning_goal)
    url = reverse("task_complete_url", kwargs={"id": single_task.pk})
    resp = client.post(url)
    assert resp.status_code == 302
    assert not SingleTask.objects.get(pk=single_task.pk).completed


def test_task_delete_view_auth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    single_task = SingleTaskFactory(learninggoal=learning_goal)
    url = reverse("task_delete_url", kwargs={"id": single_task.pk})
    client.force_login(user)
    resp = client.post(url)
    assert resp.status_code == 200
    assert not SingleTask.objects.filter(pk=single_task.pk).exists()


def test_task_delete_view_unauth(client):
    user = UserFactory()
    learning_goal = LearningGoalFactory(user=user)
    single_task = SingleTaskFactory(learninggoal=learning_goal)
    url = reverse("task_delete_url", kwargs={"id": single_task.pk})
    resp = client.post(url)
    assert resp.status_code == 302
    assert SingleTask.objects.filter(pk=single_task.pk).exists()
