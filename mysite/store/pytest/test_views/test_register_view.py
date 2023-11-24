import pytest
from django.urls import reverse
from django.test import Client
from store.models import Product
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_valid_form_submission_creates_user_and_redirects(client, db):
    form_data = {
        'username': 'newuser',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        # Add other necessary fields for your UserForm
    }
    response = client.post(reverse('register'), form_data)  # Replace 'register' with the URL name for RegisterView
    user_exists = User.objects.filter(username='newuser').exists()
    assert user_exists
    assert response.status_code == 302
    assert response.url == reverse('home')  # Ensure redirection to 'home' or your success URL


@pytest.mark.django_db
def test_invalid_form_submission_returns_errors(client, db):
    form_data = {
        'username': 'newuser',
        # Omitting password or other required fields
    }
    response = client.post(reverse('register'), form_data)
    assert 'password1' in response.context['form'].errors  # Adjust according to your form fields
    assert 'password2' in response.context['form'].errors  # Adjust according to your form fields
    assert not User.objects.filter(username='newuser').exists()


@pytest.mark.django_db
def test_register_view_uses_correct_template(client):
    response = client.get(reverse('register'))  # Replace 'register' with the URL name for RegisterView
    assert response.status_code == 200
    assert 'registration/register.html' in [t.name for t in response.templates]
