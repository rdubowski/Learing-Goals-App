import pytest
from django.urls import reverse
from pytest_django.asserts import (
    assertContains,
    assertRedirects
)

from goals.tests.test import TestCase
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

class TestWelcomePageView(TestCase):
    def test_welcome_page_view_unauth(self):
        url = reverse("welcome_screen")
        self.get_check_200(url)

    def test_welcome_page_view_auth(self):
        url = reverse("welcome_screen")
        user = self.make_user()
        
        with self.login(user):
                response = self.get(url)
                self.response_302(response)

class TesstRegisterPageView(TestCase):
    def test_register_page_view_unauth(self):
        url = reverse("register")
        self.get_check_200(url)
    
    
    def test_register_page_view_auth(self):
        url = reverse("register")
        user = self.make_user()
        
        with self.login(user):
                response = self.get(url)
                self.response_302(response)

    # def test_post(self):
    #     url = reverse("register")
    #     data = {
    #         "username": "user_test_123", 
    #         "email": "uuser_test@email.com", 
    #         "password1":"hassword123",
    #         "password2":"hassword123"
            
    #     }
    #     self.post(
    #         url_name=url,
    #         follow=True,
    #         data=data,
    #         format="text/html"
    #     )
    #     self.response_302()
class TestLoginPageView(TestCase):
    def test_login_page_view_unauth(self):
        url = reverse("login")
        self.get_check_200(url)
        self.assertLoginRequired('my-restricted-url')

    
    def test_login_page_view_auth(self):
        url = reverse("login")
        user = self.make_user()
        
        with self.login(user):
                response = self.get(url)
                self.response_302(response)


# class TestDashboardView(TestCase):
#     def test_unauthenticated_access(self):
#         url = reverse('dashboard')
#         self.assertLoginRequired('/dashboard/')