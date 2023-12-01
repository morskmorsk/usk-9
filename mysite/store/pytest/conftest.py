import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from store.models import Order, Product, OrderDetail, Review, Supplier, Location, Department, ShoppingCart, WorkOrder, Part, Device
from phonenumber_field.modelfields import PhoneNumberField
import uuid


User = get_user_model()

@pytest.fixture
def test_time():
    return timezone.now()

@pytest.fixture
def test_user(db):
    def create_user(username):
        # Ensure uniqueness by deleting any existing user with the same username
        User.objects.filter(username=username).delete()
        return User.objects.create_user(username=username, password='testpass123')
    return create_user

@pytest.fixture
def order(test_user):
    order = Order.objects.create(
        user=test_user('testuser'),
        order_date=timezone.now(),)
    return order

@pytest.fixture
def test_location():
    location = Location.objects.create(
        name='Test Location')
    return location

@pytest.fixture
def test_product(test_supplier, test_location, test_department):
    product = Product.objects.create(
        name='Test Product',
        supplier=test_supplier,
        # inventory=test_inventory,
        description='Test Product Description',
        price=Decimal('10.00'),
        sku='TESTSKU',
        department=test_department,
        location=test_location,
        url='https://www.testproduct.com',
        # is_on_sale=False,
        sale_start_date=None,
        sale_end_date=None,
    )
    return product

@pytest.fixture
def test_supplier():
    supplier = Supplier.objects.create(
        name='Test Supplier')
    return supplier

@pytest.fixture
def test_department():
    department = Department.objects.create(
        name='Test Department', taxable=True)
    return department

@pytest.fixture
def order_detail(order, test_product):
    return OrderDetail.objects.create(
        order=order,
        product=test_product,
        quantity=2,
        price=100.00
    )

@pytest.fixture
def test_shopping_cart(test_user):
    user = test_user('shoppingcarttestuser')
    return ShoppingCart.objects.create(
        user=user,
    )

@pytest.fixture
def test_work_order(test_user):
    user=test_user('workordertestuser')
    work_order_updated_at = timezone.now()
    work_order = WorkOrder.objects.create(
        user=user,
        status='pending',
        notes='Test notes',
        assigned_to=None,
        estimated_completion_date=None,
        actual_completion_date=None,
        updated_at=work_order_updated_at,
    )
    return work_order

@pytest.fixture
def test_part(test_department, test_location, test_supplier):
    part = Part.objects.create(
        name='Test Part',
        price=Decimal('10.00'),
        description='Test Part Description',
        department=test_department,
        location=test_location,
        supplier=test_supplier,
        quantity_available=10,
        quantity_reserved=2,
        sku='TESTPARTSKU',
        url='https://www.testpart.com',
    )
    return part

@pytest.fixture
def test_device(test_user, test_location, test_supplier):
    device = Device.objects.create(
        owner=test_user('testdevicetestuser'),
        name='Test Device',
        description='Test Device Description',
        grade='A',
        cost=Decimal('100.00'),
        price=Decimal('200.00'),
        sku='TESTDEVICESKU',
        imei='123456789012345',
        supplier=test_supplier,
        location=test_location,
        defect='Test Device Defect',
        url='https://www.testdevice.com',
        size='Test Device Size',
        weight='Test Device Weight',
        color='Test Device Color',
        sale_start_date=None,
        sale_end_date=None,
    )
    return device

@pytest.fixture
def test_review(test_user, test_product):
    review = Review.objects.create(
        product=test_product,
        user=test_user('testreviewtestuser'),
        rating=5,
        comment='Test Review Comment',
        review_date=timezone.now(),
    )
    return review