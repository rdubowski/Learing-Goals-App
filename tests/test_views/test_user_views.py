import pytest
from django.urls import reverse
from tests.factories import (
    UserFactory,
)
from django.contrib.auth.models import User
pytestmark = pytest.mark.django_db


def test_login_view_auth(client):
    user = UserFactory()
    url = reverse("login")
    client.force_login(user)
    resp = client.get(url)
    assert resp.status_code == 302


def test_login_view_unauth(client):
    url = reverse("login")
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'LOGIN' in str(resp.content)


def test_login_view_post(client):
    user = UserFactory()
    url = reverse("login")
    resp = client.post(url,
                       data={'username': user.username,
                             'password': user.password,
                             })
    assert resp.status_code == 200


def test_logout(client):
    user = UserFactory()
    url_logout = reverse("logout")
    url_dashboard = reverse("dashboard")
    client.force_login(user)
    resp1 = client.get(url_dashboard)
    resp2 = client.get(url_logout)
    resp3 = client.get(url_dashboard)
    assert resp1.status_code == 200
    assert resp2.status_code == 302
    assert resp3.status_code == 302


def test_register_view_auth_get(client):
    user = UserFactory()
    url = reverse("register")
    client.force_login(user)
    resp = client.get(url)
    assert resp.status_code == 302


def test_register_view_unauth_get(client):
    url = reverse("register")
    resp = client.get(url)
    assert resp.status_code == 200


def test_register_view_post(client):
    url = reverse("register")
    resp = client.post(url,
                       data={'username': 'testingname123',
                             'email': 'testemail@mail.com',
                             'password1': 'testpass123',
                             'password2': 'testpass123',
                             })
    assert resp.status_code == 302
    assert User.objects.count() == 1


def test_update_user(client):
    user = UserFactory()
    url = reverse("update_profile", kwargs={'pk': user.pk})
    client.force_login(user)
    resp1 = client.get(url)
    assert resp1.status_code == 200


def test_update_user_unauth(client):
    user = UserFactory()
    url = reverse("update_profile", kwargs={'pk': user.pk})
    resp1 = client.get(url)
    assert resp1.status_code == 302



def test_update_user(client):
    user = UserFactory()
    url = reverse("update_profile", kwargs={'pk': user.pk})
    client.force_login(user)
    resp = client.post(url,
                       data={'username': 'testingname123',
                             'email': 'testemail@mail.com',
                             'password1': user.password,
                             'password2': user.password,
                             })
    assert resp.status_code == 302
    assert User.objects.get(pk=1).username == "testingname123"
    assert User.objects.get(pk=1).email == "testemail@mail.com"
    assert User.objects.count() == 1
