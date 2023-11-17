import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from store.models import UserProfile

User = get_user_model()

@pytest.fixture
def new_user(db):
    def create_user(username):
        # Ensure uniqueness by deleting any existing user with the same username
        User.objects.filter(username=username).delete()
        return User.objects.create_user(username=username, password='testpass123')
    return create_user

@pytest.mark.django_db
def test_create_user_profile(new_user):
    user = new_user('testuser1')
    # Ensure no existing UserProfile for this user
    UserProfile.objects.filter(user=user).delete()
    
    profile = UserProfile.objects.create(
        user=user,
        address='123 Main Street',
        city='Anytown',
        state='NY',
        zip_code='12345',
        phone='+1234567890',
        bio='Test Bio',
        additional_info='Additional Info'
    )

    assert profile.user == user
    assert profile.address == '123 Main Street'
    assert profile.city == 'Anytown'
    assert profile.state == 'NY'
    assert profile.zip_code == '12345'
    assert profile.phone == '+1234567890'
    assert profile.bio == 'Test Bio'
    assert profile.additional_info == 'Additional Info'

@pytest.mark.django_db
def test_user_profile_str(new_user):
    user = new_user('testuser2')
    # Ensure no existing UserProfile for this user
    UserProfile.objects.filter(user=user).delete()

    profile = UserProfile.objects.create(user=user)
    assert str(profile) == 'testuser2\'s profile'

@pytest.mark.django_db
def test_invalid_phone_number(new_user):
    user = new_user('testuser3')
    # Ensure no existing UserProfile for this user
    UserProfile.objects.filter(user=user).delete()

    profile = UserProfile(user=user, phone='invalid')
    with pytest.raises(ValidationError):
        profile.full_clean()  # full_clean() is used to validate the model
