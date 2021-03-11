import pytest
from django.urls import reverse
from pytest_django.asserts import (
    assertContains,
    assertRedirects
)
from django.contrib.auth.models import AnonymousUser
from goals.models import LearningGoal, SingleTask
from goals.views import (
    welcome_screen,
    register_page,
    login_page,
    logout_page,
    dashboard,
    dashboard_table,
    create_goal,
    delete_goal,
    change_goal_name,
    learning_goal_tasks,
    task_complete,
    task_delete
)
from django.contrib.auth.models import User
from goals.tests.factories import (
    UserFactory,
    LearningGoalFactory,
    SingleTaskFactory
)
from django.contrib.auth.models import User
from django.test import Client


pytestmark = pytest.mark.django_db
@pytest.fixture
def user_client(django_user_model):
    """
    User fixture for tests with unprivileged user
    """
    example_user = UserFactory.build()
    created_user = django_user_model.objects.create_user(example_user)
    return created_user


def test_welcome_page_view_unauth(client):
    url = reverse("welcome_screen")
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'This is a simple app to manage your tasks.' in str(resp.content)


def test_welcome_page_view_auth(client):
    user = UserFactory()
    url = reverse("welcome_screen")
    client.force_login(user)
    resp = client.get(url)
    assert resp.status_code == 302


def test_login_view_unauth(client):
    url = reverse("login")
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'LOGIN' in str(resp.content)


def test_login_view_auth(client):
    user = UserFactory()
    url = reverse("login")
    client.force_login(user)
    resp = client.get(url)
    assert resp.status_code == 302
      

def test_logout(client):
    user = UserFactory()
    url_logout = reverse("logout")
    url_dashboard = reverse("login")
    client.force_login(user)
    resp = client.get(url_logout)
    resp2 = client.get(url_dashboard)
    assert resp.status_code == 302
    assert resp2.status_code == 200


def test_register_view_unauth(client):
    url = reverse("register")
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'REGISTER ACCOUNT' in str(resp.content)


def test_register_view_auth(client):
    user = UserFactory()
    url = reverse("register")
    client.force_login(user)
    resp = client.get(url)
    assert resp.status_code == 302


def test_dashboard_view_unauth_redirect(client):
    url = reverse("dashboard")
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


def test_dashboard_table_view_unauth(client):
    url = reverse("dashboard_table")
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
    resp = client.post(url, data={'name': 'learnname'})
    assert resp.status_code == 302
    assert LearningGoal.objects.get(pk=1).name == 'learnname'


def test_create_goal_view_unauth_post(client):
    url = reverse("create_goal")
    resp = client.post(url, data={'name': 'learnname'})
    assert resp.status_code == 302
    assert LearningGoal.objects.count() == 0
