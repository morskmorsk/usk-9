import pytest
from django.utils import timezone
from store.models import DeviceManufacturer

@pytest.mark.django_db
def test_create_device_manufacturer():
    manufacturer_name = "Tech Innovations Inc."
    description = "Leading manufacturer in tech gadgets."
    url = "https://www.techinnovations.com"

    manufacturer = DeviceManufacturer.objects.create(
        name=manufacturer_name,
        description=description,
        url=url
    )

    assert manufacturer.name == manufacturer_name
    assert manufacturer.description == description
    assert manufacturer.url == url
    assert manufacturer.created_at <= timezone.now()
    assert manufacturer.updated_at <= timezone.now()

@pytest.mark.django_db
def test_device_manufacturer_str():
    manufacturer = DeviceManufacturer.objects.create(name="GadgetPro")
    assert str(manufacturer) == "GadgetPro"

@pytest.mark.django_db
def test_device_manufacturer_blank_fields():
    manufacturer = DeviceManufacturer.objects.create(name="SimpleTech")
    
    assert manufacturer.description is None
    assert manufacturer.url is None
