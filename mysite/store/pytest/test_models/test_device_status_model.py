import pytest
from django.utils import timezone
from store.models import DeviceStatus

@pytest.mark.django_db
def test_create_device_status():
    status_name = "Active"
    description = "The device is actively being used."

    status = DeviceStatus.objects.create(
        name=status_name,
        description=description
    )

    assert status.name == status_name
    assert status.description == description
    assert status.created_at <= timezone.now()
    assert status.updated_at <= timezone.now()

@pytest.mark.django_db
def test_device_status_str():
    status = DeviceStatus.objects.create(name="Inactive")
    assert str(status) == "Inactive"

@pytest.mark.django_db
def test_device_status_blank_fields():
    status = DeviceStatus.objects.create(name="Maintenance Mode")
    
    assert status.description is None
