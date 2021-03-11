import pytest
from django.urls import reverse
from goals.tests.factories import (
    UserFactory,
)

pytestmark = pytest.mark.django_db


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
    url_dashboard = reverse("dashboard")
    client.force_login(user)
    resp1 = client.get(url_dashboard)
    resp2 = client.get(url_logout)
    resp3 = client.get(url_dashboard)
    assert resp1.status_code == 200
    assert resp2.status_code == 302
    assert resp3.status_code == 302


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
