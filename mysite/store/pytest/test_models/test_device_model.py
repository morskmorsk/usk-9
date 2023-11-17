from django.utils import timezone
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from store.models import Device, DeviceModel, Department, Supplier, Location, DeviceDefect

# Fixtures for the related models
@pytest.fixture
def device_model(db):
    # Assuming necessary fields and creation for DeviceModel
    return DeviceModel.objects.create(name="Model X")

@pytest.fixture
def department(db):
    # Assuming necessary fields and creation for Department
    return Department.objects.create(name="Electronics")

@pytest.fixture
def supplier(db):
    # Assuming necessary fields and creation for Supplier
    return Supplier.objects.create(name="Tech Supplier")

@pytest.fixture
def location(db):
    # Assuming necessary fields and creation for Location
    return Location.objects.create(name="Warehouse 1")

@pytest.fixture
def device_defect(db):
    # Assuming necessary fields and creation for DeviceDefect
    return DeviceDefect.objects.create(defect_name="Screen Issue")


# Test for creating a Device instance
@pytest.mark.django_db
def test_create_device(device_model, department, supplier, location, device_defect):
    name = "Gadget X"
    condition = "New"
    description = "Latest model of Gadget X"
    price = 499.99
    sku = "GX-2023"
    imei = "123456789012345"
    image = SimpleUploadedFile("device.jpg", b"file_content", content_type="image/jpeg")
    url = "https://www.example.com/gadget-x"
    size = "15x10x5"
    weight = "1.5kg"
    color = "Black"

    device = Device.objects.create(
        name=name,
        device_model=device_model,
        condition=condition,
        description=description,
        price=price,
        sku=sku,
        department=department,
        imei=imei,
        supplier=supplier,
        location=location,
        image=image,
        defect=device_defect,
        url=url,
        size=size,
        weight=weight,
        color=color
    )

    assert device.name == name
    assert device.condition == condition
    assert device.description == description
    assert device.price == price
    assert device.sku == sku
    assert device.imei == imei
    assert device.image  # Check if image is uploaded
    assert device.url == url
    assert device.size == size
    assert device.weight == weight
    assert device.color == color
    assert device.created_at <= timezone.now()
    assert device.updated_at <= timezone.now()

# Test for string representation of Device
@pytest.mark.django_db
def test_device_str(device_model, department, location):
    device = Device.objects.create(
        name="Device Y",
        sku="DY-2023",
        device_model=device_model,
        department=department,
        location=location,
        price=100.00  # Add a default price to satisfy the NOT NULL constraint
    )
    assert str(device) == "Device Y - SKU: DY-2023"