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

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_client(django_user_model):
    """
    User fixture for tests with unprivileged user
    """
    example_user = UserFactory.build()
    created_user = django_user_model.objects.create_user(example_user)
    return created_user


def test_welcome_page_view_unauth(rf):
    url = reverse("welcome_screen")
    request = rf.get(url)
    request.user = AnonymousUser()
    response = welcome_screen(request)
    assert response.status_code == 200

