import pytest
from django.urls import reverse
from django.test import Client


def test_login_required_to_access_view(client):
    url = reverse('home')  # Replace 'product_list' with the actual name of your ProductListView URL
    response = client.get(url)
    assert response.status_code == 302  # Redirects unauthenticated user


def test_context_data_for_authenticated_user(client, test_user, test_product):
    user=test_user('testuser')
    client.force_login(user)
    url = reverse('home')
    response = client.get(url)
    assert test_product in response.context['products']
    assert response.status_code == 200


def test_correct_template_used(client, test_user):
    user=test_user('testuser')
    client.force_login(user)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'store/product_list.html' in [t.name for t in response.templates]
