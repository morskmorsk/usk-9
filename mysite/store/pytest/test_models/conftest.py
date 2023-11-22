import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from store.models import Order, Product, OrderDetail, Supplier, Location, Inventory, Department, Return, ShoppingCart, WorkOrder, Part, Service, ServiceDetail, WorkOrderDetail
from phonenumber_field.modelfields import PhoneNumberField
import uuid


User = get_user_model()

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
        is_on_sale=False,
        sale_start_date=None,
        sale_end_date=None,
    )
    return product


@pytest.fixture
def test_inventory(test_location, test_product):
    inventory = Inventory.objects.create(
        product=test_product,
        location=test_location,
        quantity_available=10,
        quantity_reserved=2,
    )
    return inventory

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
def test_return(order, test_product, test_user):
    user=test_user('returntestuser')
    return_obj = Return.objects.create(
        order=order,
        product=test_product,
        user=user,
        reason='Test reason',
        condition='Test condition',
    )
    return return_obj


@pytest.fixture
def test_shopping_cart(test_user):
    user = test_user('testuser')
    return ShoppingCart.objects.create(
        customer=user,
    )


@pytest.fixture
def test_work_order(test_user):
    user=test_user('workordertestuser')
    work_order_created_at = timezone.now()
    work_order_updated_at = timezone.now()
    work_order = WorkOrder.objects.create(
        customer=user,
        status='pending',
        notes='Test notes',
        assigned_to=None,
        estimated_completion_date=None,
        actual_completion_date=None,
        created_at=work_order_created_at,
        updated_at=work_order_updated_at,
    )
    return work_order


@pytest.fixture
def test_service(test_user, test_work_order):
    user=test_user('servicetestuser')
    service = Service.objects.create(
        name='Test Service',
        description='Test Service Description',
        work_order=test_work_order,
        technician=user,
    )
    return service


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
def test_service_detail(test_service, test_part):
    service_detail = ServiceDetail.objects.create(
        service=test_service,
        # part=test_part,
        service_description='Test Service Description',
        part_cost=Decimal('10.00'),
        service_cost=Decimal('10.00'),
    )
    return service_detail


@pytest.fixture
def test_work_order_detail(test_work_order, test_service_detail):
    work_order_detail = WorkOrderDetail.objects.create(
        work_order=test_work_order,
        service_detail=test_service_detail,
        Part=None,
    )
    return work_order_detail
