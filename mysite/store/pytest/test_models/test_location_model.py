import pytest
from django.utils import timezone
from store.models import Location

@pytest.mark.django_db
def test_create_location():
    location_name = "Downtown Office"
    location_address = "123 Main St, Metropolis"
    location_description = "Main corporate office"

    location = Location.objects.create(
        name=location_name,
        address=location_address,
        description=location_description
    )

    assert location.name == location_name
    assert location.address == location_address
    assert location.description == location_description
    assert location.created_at <= timezone.now()
    assert location.updated_at <= timezone.now()

@pytest.mark.django_db
def test_location_str():
    location = Location.objects.create(name="Warehouse", address="456 Elm St")
    expected_str = "Warehouse at 456 Elm St"
    
    assert str(location) == expected_str

@pytest.mark.django_db
def test_location_blank_fields():
    location = Location.objects.create()  # No arguments, blank fields

    assert location.name is None
    assert location.address is None
    assert location.description is None
    assert location.created_at <= timezone.now()
    assert location.updated_at <= timezone.now()
