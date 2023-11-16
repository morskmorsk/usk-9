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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Created on {self.created_at.strftime('%Y-%m-%d')})"


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Added on {self.created_at.strftime('%Y-%m-%d')})"


class Location(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} at {self.address}"


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.PhoneNumberField(blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.name} - Contact: {self.contact_info if self.contact_info else 'N/A'}"


class DeviceDefect(models.Model):
    defect_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    report = models.TextField(blank=True, null=True)
    defect_fix = models.TextField(blank=True, null=True)
    repair = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.name


class Device_IMEI(models.Model):
    imei = models.CharField(max_length=15, blank=True, null=True)
    imei_status = models.CharField(max_length=255, blank=True, null=True)
    report = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.name


class DeviceManufacturer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DeviceStatus(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DeviceGrade(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DeviceModel(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(DeviceManufacturer, on_delete=models.CASCADE)
    model_number = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    status = models.ForeignKey
    grade = models.ForeignKey(DeviceGrade, on_delete=models.CASCADE)
    warranty_period = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.manufacturer.name} {self.name} - {self.model_number}"

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=255)
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    condition = models.CharField(max_length=255 , blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    imei = models.OneToOneField(Device_IMEI, on_delete=models.CASCADE, blank=True, null=True)
    supplier = models.ManyToManyField(Supplier, through='ProductSupplier')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    defect = models.OneToManyField(DeviceDefect, on_delete=models.CASCADE, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - SKU: {self.sku}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    # imei = models.CharField(max_length=15, blank=True, null=True)      
    supplier = models.ManyToManyField(Supplier, through='ProductSupplier', blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    is_on_sale = models.BooleanField(default=False)
    sale_start_date = models.DateTimeField(blank=True, null=True)
    sale_end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - Price: {self.price}"

class ProductSupplier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'supplier')

    # def save(self, *args, **kwargs):
    # # Custom validation logic
    #     if some_condition_not_met:
    #         raise ValidationError("Custom error message")

    #     super(ProductSupplier, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} supplied by {self.supplier.name}"

PAYMENT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('refunded', 'Refunded'),
)
class Payment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    payment_gateway = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} - {self.payment_status}"

ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)  # Allows guest checkout with no user attached
    status = models.CharField(max_length=255, default='pending')
    order_date = models.DateTimeField(default=timezone.now)
    payment_date = models.DateTimeField(blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=255, blank=True, null=True)
    shipping_state = models.CharField(max_length=2, blank=True, null=True)
    shipping_zip_code = models.CharField(max_length=5, blank=True, null=True)
    shipping_phone = models.PhoneNumberField(blank=True, null=True)
    shipping_method = models.CharField(max_length=255, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    tracking_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} - Status: {self.status}"

    def subtotal(self):
        return sum(item.product.price * item.quantity for item in self.details.all())
    
    def tax(self):
        return self.subtotal() * 0.07
    
    def total(self):
        return self.subtotal() + self.tax() + self.shipping_cost
    
    def shipping_cost(self):
        return 5.00
    
    def shipping_method(self):
        return "USPS"
    
    def shipping_address(self):
        return self.user.address
    
    def shipping_city(self):
        return self.user.city
    
    def shipping_state(self):
        return self.user.state
    
    def shipping_zip_code(self):
        return self.user.zip_code
    
    def shipping_phone(self):
        return self.user.phone

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"Detail for Order {self.order.id} - Product: {self.product.name}"

CONDITION_CHOICES = (
    ('new', 'New'),
    ('used', 'Used'),
    ('damaged', 'Damaged'),
)

class Return(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reason = models.TextField()
    return_date = models.DateTimeField(default=timezone.now)
    condition = models.CharField(max_length=255)
    restocking_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    condition = models.CharField(max_length=255, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    refund_processed = models.BooleanField(default=False)
    refund_transaction_id = models.CharField(max_length=255, blank=True, null=True)

    # def process_refund(self):
    #     if not self.refund_processed:
    #         # Implement refund logic here
    #         # This could involve calling an external payment gateway API
    #         refund_id = call_payment_gateway_for_refund(self.order, self.refund_amount)
    #         self.refund_transaction_id = refund_id
    #         self.refund_processed = True
    #         self.save()
    #     else:
    #         raise ValueError("Refund already processed for this return")


    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the return is new; if so, calculate restocking fee
            self.restocking_fee = self.product.price * 0.15
        super(Return, self).save(*args, **kwargs)
        # You would typically also update inventory and process the refund here, depending on your workflow

    def __str__(self):
        return f"Return for {self.product.name} by {self.user.user.username} - Condition: {self.condition}"


LOW_STOCK_THRESHOLD = 10  # You can adjust this value as needed

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity_available = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_inventory(self):
        return self.quantity_available - self.quantity_reserved

    def is_stock_low(self):
        return self.quantity_available <= LOW_STOCK_THRESHOLD

    def __str__(self):
        return f"{self.product.name} in {self.location.name} - Available: {self.quantity_available}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.user.username} - Rating: {self.rating}"

# Handling Abandoned Carts

# Consider implementing a mechanism to identify and handle abandoned carts,
# such as sending reminder emails to users or automatically clearing carts after a certain period.
# Linking Cart with User Session

# If not already done, ensure that the shopping cart is linked to the user's session,
# especially for guest users. This typically involves session management in Django.
# Adding Additional Features

# Think about additional features that might enhance the shopping experience,
# such as saving items for later, wishlists, or recommendations based on cart contents.

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
        return f"Shopping Cart for {self.customer.user.username}"


class ShoppingCartDetail(models.Model):
    cart = models.ForeignKey(ShoppingCart, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(10)])   
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def item_subtotal(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if self.pk:
            old_item = ShoppingCartDetail.objects.get(pk=self.pk)
            if old_item.quantity != self.quantity:
                # Update inventory reservation based on the new quantity
                difference = self.quantity - old_item.quantity
                product_inventory = Inventory.objects.get(product=self.product)
                product_inventory.quantity_reserved += difference
                product_inventory.save()
        super(ShoppingCartDetail, self).save(*args, **kwargs)

    def __str__(self):
        return f"Item: {self.product.name} in Cart {self.cart.id} - Quantity: {self.quantity}"

WORK_ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('on_hold', 'On Hold'),
)

class WorkOrder(models.Model):
    customer = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=WORK_ORDER_STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(UserProfile, related_name='assigned_orders', on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    estimated_completion_date = models.DateTimeField(blank=True, null=True)
    actual_completion_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_cost(self):
        return sum(item.service_cost * item.quantity for item in self.details.all()) + sum(item.part_cost * item.quantity for item in self.details.all())
    
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


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    technician = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    service_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class Part(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity_available = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class ServiceDetail(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True)
    service_description = models.TextField(default='repair')
    service_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    part_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Detail for Service {self.service.name}"

class WorkOrderDetail(models.Model):
    work_order = models.ForeignKey(WorkOrder, related_name='details', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def quantity_changed(self):
        return self.quantity != self.quantity
    
    def __str__(self):
        return f"Work Order {self.work_order.id} Detail - Part: {self.part.name if self.part else 'N/A'}"

