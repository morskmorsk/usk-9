import pytest
from django.urls import reverse
from django.test import Client
from store.models import Product

@pytest.mark.django_db
def test_login_required_for_product_detail_view(client, test_product):
    url = reverse('product-detail', args=[test_product.id])  # Replace 'product_detail' with your URL name
    response = client.get(url)
    assert response.status_code == 302  # Expecting a redirect for unauthenticated users


@pytest.mark.django_db
def test_product_detail_view_returns_correct_product(client, test_user, test_product):
    user = test_user('testuser')
    client.force_login(user)
    url = reverse('product-detail', args=[test_product.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['product'] == test_product


def test_product_detail_view_uses_correct_template(client, test_user, test_product):
    user= test_user('testuser')
    client.force_login(user)
    url = reverse('product-detail', args=[test_product.id])
    response = client.get(url)
    assert 'store/product_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_product_detail_view_context_data(client, test_user, test_product):
    user= test_user('testuser')
    client.force_login(user)
    url = reverse('product-detail', args=[test_product.id])
    response = client.get(url)
    assert 'product' in response.context
    assert response.context['product'] == test_product
