import pytest
from django.urls import reverse, resolve
from goals.views import welcome_screen


pytestmark = pytest.mark.django_db


def test_welcome_url():
    url = reverse('welcome_screen')
    assert url == "/"


def test_login_url():
    url = reverse('login')
    assert url == "/login/"

def test_register_url():
    url = reverse('register')
    assert url == "/register/"

def test_dashboard_url():
    url = reverse('dashboard')
    assert url == "/dashboard/"

