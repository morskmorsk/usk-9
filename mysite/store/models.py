from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('P', 'Prefer not to say'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=5, blank=True, null=True)
    phone = models.PhoneNumberField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}'s profile"


class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    taxable = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images', blank=True, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=255, default='default location')
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, default='default address')

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.PhoneNumberField(blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=5)


    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    imei = models.CharField(max_length=15, blank=True, null=True)
    imei_status = models.CharField(max_length=255, blank=True, null=True)
    report = models.TextField(blank=True, null=True)
    supplier = models.ManyToManyField(Supplier, through='ProductSupplier')
    # location = models.ForeignKey(Location, on_delete=models.CASCADE)
    location = models.ManyToManyField(Location, through='Inventory')
    image = models.ImageField(upload_to='product_images', blank=True, null=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    # IMEI is optional, as not all products are devices.
    imei = models.CharField(max_length=15, blank=True, null=True)      
    supplier = models.ManyToManyField(Supplier, through='ProductSupplier', blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    # location = models.ManyToManyField(Location, through='Inventory')
    image = models.ImageField(upload_to='product_images', blank=True, null=True)

    def __str__(self):
        return self.name


class ProductSupplier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.supplier.name}"


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity_available = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} at {self.location.address}"


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)  # Allows guest checkout with no user attached
    status = models.CharField(max_length=255, default='pending')
    order_date = models.DateTimeField(default=timezone.now)
    # Other fields as necessary

    def __str__(self):
        return f"Order {self.id}"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail for Order {self.order.id}"


class Payment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment for Order {self.order.id}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.user.username}"


class Return(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reason = models.TextField()
    return_date = models.DateTimeField(default=timezone.now)
    condition = models.CharField(max_length=255)
    restocking_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the return is new; if so, calculate restocking fee
            self.restocking_fee = self.product.price * 0.15
        super(Return, self).save(*args, **kwargs)
        # You would typically also update inventory and process the refund here, depending on your workflow

    def __str__(self):
        return f"Return for {self.product.name} by {self.user.user.username}"


class ShoppingCart(models.Model):
    customer = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def tax(self):
        return sum(item.product.price * item.quantity for item in self.details.all()) * 0.07

    def subtotal(self):
        return sum(item.product.price * item.quantity for item in self.details.all())

    def total(self):
        return self.subtotal() + self.tax()

    def __str__(self):
        return f"Shopping Cart for {self.user.username}"


class ShoppingCartDetail(models.Model):
    cart = models.ForeignKey(ShoppingCart, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Detail for Shopping Cart {self.cart.id}"


class WorkOrder(models.Model):
    customer = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Work Order {self.id} - {self.status}"


class WorkOrderDetail(models.Model):
    work_order = models.ForeignKey(WorkOrder, related_name='details', on_delete=models.CASCADE)
    part = models.ForeignKey(Product, limit_choices_to={'department__name': 'part'}, on_delete=models.SET_NULL, null=True, blank=True)
    device = models.TextField()
    service_description = models.TextField(default='repair')
    service_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    part_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    service_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Detail for Work Order {self.work_order.id}"


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)

    def __str__(self):
        return self.name


class ServiceDetail(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail for Service {self.service.name}"
