import pytest
from django.contrib.auth import get_user_model
from store.models import UserProfile
from django.utils import timezone
from decimal import Decimal
from store.models import Order, UserProfile, Product, OrderDetail, Supplier, Location, Inventory, Department, Return, ShoppingCart, WorkOrder, Part, Service, ServiceDetail, WorkOrderDetail
from phonenumber_field.modelfields import PhoneNumberField
import uuid


User = get_user_model()


@pytest.fixture
def test_time():
    return timezone.now()

@pytest.fixture
def new_user(db):
    def create_user(username):
        # Ensure uniqueness by deleting any existing user with the same username
        User.objects.filter(username=username).delete()
        return User.objects.create_user(username=username, password='testpass123')
    return create_user


@pytest.fixture
def new_user_profile(db, new_user):
    def create_user_profile(username):
        user = new_user(username)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        return user_profile
    return create_user_profile


@pytest.fixture
def order(new_user_profile):
    order = Order.objects.create(
        user=new_user_profile('testuser'),
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


# class Inventory(models.Model):
#     product = models.OneToOneField(Product, on_delete=models.CASCADE)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
#     quantity_available = models.IntegerField(default=0)
#     quantity_reserved = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
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
def test_return(order, test_product, new_user_profile):
    user=new_user_profile('returntestuser')
    return_obj = Return.objects.create(
        order=order,
        product=test_product,
        user=user,
        reason='Test reason',
        condition='Test condition',
    )
    return return_obj


@pytest.fixture
def test_shopping_cart(new_user_profile):
    user = new_user_profile('testuser')
    return ShoppingCart.objects.create(
        customer=user,
    )


@pytest.fixture
def test_work_order(new_user_profile):
    user=new_user_profile('workordertestuser')
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

# class Service(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
#     technician = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     service_date = models.DateTimeField(auto_now_add=True)


@pytest.fixture
def test_service(new_user_profile, test_work_order):
    user=new_user_profile('servicetestuser')
    service = Service.objects.create(
        name='Test Service',
        description='Test Service Description',
        work_order=test_work_order,
        technician=user,
    )
    return service

# class Part(models.Model):
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
#     quantity_available = models.IntegerField(default=0)
#     quantity_reserved = models.IntegerField(default=0)
#     sku = models.CharField(max_length=255)
#     url = models.URLField(blank=True, null=True)
#     image = models.ImageField(upload_to='product_images', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


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
    

# class ServiceDetail(models.Model):
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     # part = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True)
#     service_description = models.TextField(default='repair')
#     part_cost = models.DecimalField(max_digits=10, decimal_places=2, default=888.88)
#     service_cost = models.DecimalField(max_digits=10, decimal_places=2, default=888.88)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

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

# class WorkOrderDetail(models.Model):
#     work_order = models.ForeignKey(WorkOrder, related_name='details', on_delete=models.CASCADE)
#     service_detail = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE)
#     part= models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


@pytest.fixture
def test_work_order_detail(test_work_order, test_service_detail):
    work_order_detail = WorkOrderDetail.objects.create(
        work_order=test_work_order,
        service_detail=test_service_detail,
        Part=None,
    )
    return work_order_detail
