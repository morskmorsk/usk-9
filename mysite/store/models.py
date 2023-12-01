from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# /////////////////////////////////////////////////////////////////////////////////
User = get_user_model()
# /////////////////////////////////////////////////////////////////////////////////
TAX_RATE = Decimal('0.09')
LOW_STOCK_THRESHOLD = 10
# /////////////////////////////////////////////////////////////////////////////////
ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

WORK_ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('on_hold', 'On Hold'),
)

DEVICE_GRADE_CHOICES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
]

# //////////////////////////////////////////////////////////////////////////////////////////
class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    taxable = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} - Taxable: {self.taxable}"

    class Meta:
        verbose_name_plural = 'Departments'
        ordering = ['id']


class Location(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} at {self.address}"

    class Meta:
        verbose_name_plural = 'Locations'
        ordering = ['id']
  

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = PhoneNumberField(blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=5, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.name} - Contact: {self.contact_info if self.contact_info else 'N/A'}"

    class Meta:
        verbose_name_plural = 'Suppliers'
        ordering = ['id']


class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    issues = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    grade = models.CharField(max_length=255 , blank=True, null=True, choices=DEVICE_GRADE_CHOICES)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255, unique=True)
    imei = models.CharField(max_length=15, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    defect = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    sale_start_date = models.DateTimeField(blank=True, null=True)
    sale_end_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_for_sale = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - SKU: {self.sku}"
    
    def is_on_sale(self):
        return self.sale_start_date <= timezone.now() <= self.sale_end_date

    class Meta:
        verbose_name_plural = 'Devices'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)
    imei = models.CharField(max_length=15, blank=True, null=True)
    on_hand_quantity = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    sale_start_date = models.DateTimeField(blank=True, null=True)
    sale_end_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - Price: {self.price:.2f}"

    def is_on_sale(self):
        return self.sale_start_date <= timezone.now() <= self.sale_end_date
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['id']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Allows guest checkout with no user attached
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=255, blank=True, null=True)
    shipping_state = models.CharField(max_length=2, blank=True, null=True)
    shipping_zip_code = models.CharField(max_length=5, blank=True, null=True)
    shipping_phone = PhoneNumberField(blank=True, null=True)
    shipping_method = models.CharField(max_length=255, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    tracking_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - Status: {self.status}"
    
    class Meta:
        verbose_name_plural = 'Orders'
        ordering = ['-order_date']


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"Detail for Order {self.order.id} - Product: {self.product.name}"

    class Meta:
        verbose_name_plural = 'Order Details'
        ordering = ['id']


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.user.username} - Rating: {self.rating}"
    
    class Meta:
        ordering = ['-review_date']
        unique_together = ['product', 'user']
        verbose_name_plural = 'Reviews'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_subtotal(self):
        subtotal = Decimal('0.00')
        for item in self.details.all():
            subtotal += item.price
        return subtotal
    
    def calculate_tax(self):
        tax = Decimal('0.00')
        tax = self.calculate_subtotal() * TAX_RATE
        return tax

    def calculate_total(self):
        total = Decimal('0.00')
        total = self.calculate_subtotal() + self.calculate_tax()
        return total

    def __str__(self):
        return f"Shopping Cart for {self.user.username}"

    class Meta:
        verbose_name_plural = 'Shopping Carts'
        ordering = ['id']


class ShoppingCartDetail(models.Model):
    cart = models.ForeignKey(ShoppingCart, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(10)])   
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def item_tax(self):
        try:
            product_department = self.product.department
            if product_department.taxable:
                return self.price * TAX_RATE  # TAX_RATE is a Decimal object
            else:
                return Decimal('0.00')
        except:
            return Decimal('999.99')

    def item_total(self):
        try:
            return self.price + self.item_tax()
        except:
            return Decimal('999.99')

    def __str__(self):
        return f"Item: {self.product.name} in Cart {self.cart.id} - Quantity: {self.quantity}"

    class Meta:
        verbose_name_plural = 'Shopping Cart Details'
        ordering = ['id']


class WorkOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    problem = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=WORK_ORDER_STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(User, related_name='assigned_orders', on_delete=models.SET_NULL, null=True, blank=True)
    estimated_completion_date = models.DateTimeField(blank=True, null=True)
    actual_completion_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_cost(self):
        pass
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_order = WorkOrder.objects.get(pk=self.pk)
            if old_order.status != self.status:
                # Handle status change
                self.send_status_update_notification()
        super(WorkOrder, self).save(*args, **kwargs)

    def send_status_update_notification(self):
        # Logic to send notifications (e.g., email, SMS, internal message)
        pass

    def __str__(self):
        return f"Work Order {self.id} - Status: {self.get_status_display()}"

    class Meta:
        verbose_name_plural = 'Work Orders'
        ordering = ['id']


class Part(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity_available = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)
    sku = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Parts'
        ordering = ['id']