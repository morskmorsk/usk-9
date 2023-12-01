import pytest
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from store.models import Product, Department, Supplier, Location

# # Fixtures for the related models
# @pytest.fixture
# def department(db):
#     return Department.objects.create(name="Electronics")

# @pytest.fixture
# def supplier(db):
#     return Supplier.objects.create(name="Tech Supplier")

# @pytest.fixture
# def location(db):
#     return Location.objects.create(name="Warehouse 1")

# Test for creating a Product instance
@pytest.mark.django_db
def test_create_product(test_department, test_supplier, test_location):
    name = "Gadget Y"
    description = "Advanced tech gadget Y"
    price = 199.99
    sku = "GY-2023"
    department = test_department
    supplier = test_supplier
    location = test_location
    image = SimpleUploadedFile("product.jpg", b"file_content", content_type="image/jpeg")
    url = "https://www.example.com/gadget-y"

    product = Product.objects.create(
        name=name,
        description=description,
        price=price,
        sku=sku,
        department=department,
        supplier=supplier,
        location=location,
        image=image,
        url=url,
        # is_on_sale=False,
        # updated_at=timezone.now(),
    )

    assert product.name == name
    assert product.description == description
    assert product.price == price
    assert product.sku == sku
    assert product.department == department
    assert product.supplier == supplier
    assert product.location == location
    assert product.image  # Check if image is uploaded
    assert product.url == url
    # assert product.is_on_sale == False
    # assert product.updated_at == updated_at

# Test for string representation of Product
@pytest.mark.django_db
def test_product_str(test_department, test_supplier, test_location):
    department = test_department
    supplier = test_supplier
    location = test_location
    product = Product.objects.create(
        name="Product Z",
        price=50.00,
        sku="PZ-2023",
        department=department,
        supplier=supplier,
        location=location
    )
    expected_str = "Product Z - Price: 50.00"
    assert str(product) == expected_str
