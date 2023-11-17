import pytest
from django.utils import timezone
from store.models import DeviceModel, DeviceManufacturer, DeviceStatus, DeviceGrade

@pytest.fixture
def device_manufacturer(db):
    return DeviceManufacturer.objects.create(name="Tech Manufacturer")

@pytest.fixture
def device_status(db):
    return DeviceStatus.objects.create(name="Active")

@pytest.fixture
def device_grade(db):
    return DeviceGrade.objects.create(name="Premium")

@pytest.mark.django_db
def test_create_device_model(device_manufacturer, device_status, device_grade):
    model_name = "Model X1"
    model_number = "X1-2023"
    warranty_period = "2 years"
    description = "Advanced tech model."
    url = "https://www.example.com/model-x1"

    device_model = DeviceModel.objects.create(
        name=model_name,
        manufacturer=device_manufacturer,
        model_number=model_number,
        status=device_status,
        grade=device_grade,
        warranty_period=warranty_period,
        description=description,
        url=url
    )

    assert device_model.name == model_name
    assert device_model.manufacturer == device_manufacturer
    assert device_model.model_number == model_number
    assert device_model.status == device_status
    assert device_model.grade == device_grade
    assert device_model.warranty_period == warranty_period
    assert device_model.description == description
    assert device_model.url == url
    assert device_model.created_at <= timezone.now()
    assert device_model.updated_at <= timezone.now()

@pytest.mark.django_db
def test_device_model_str(device_manufacturer):
    device_model = DeviceModel.objects.create(
        name="Model Y", 
        manufacturer=device_manufacturer, 
        model_number="Y-2021"
    )
    expected_str = f"{device_manufacturer.name} Model Y - Y-2021"
    assert str(device_model) == expected_str
