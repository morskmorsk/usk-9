import pytest
from store.models import ProductSupplier, Product, Supplier, Department, Location

@pytest.fixture
def department(db):
    return Department.objects.create(name="Electronics")

@pytest.fixture
def location(db):
    return Location.objects.create(name="Main Warehouse")  # Ensure this instance is created correctly

@pytest.fixture
def product(department, location):  # Include location fixture
    return Product.objects.create(name="Product Z", price=50.00, department=department, location=location)

@pytest.fixture
def supplier(db):
    return Supplier.objects.create(name="Supplier Z")

# Test for creating a ProductSupplier instance
@pytest.mark.django_db
def test_create_product_supplier(product, supplier):
    product_supplier = ProductSupplier.objects.create(
        product=product,
        supplier=supplier
    )

    assert product_supplier.product == product
    assert product_supplier.supplier == supplier
    assert product_supplier.created_at is not None
    assert product_supplier.updated_at is not None

# Test for string representation of ProductSupplier
@pytest.mark.django_db
def test_product_supplier_str(product, supplier):
    product_supplier = ProductSupplier.objects.create(
        product=product,
        supplier=supplier
    )
    expected_str = f"{product.name} supplied by {supplier.name}"
    assert str(product_supplier) == expected_str
