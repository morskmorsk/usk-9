from django.utils import timezone
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from store.models import Device

# create pytest tests for the following model:
# class Device(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     grade = models.CharField(max_length=255 , blank=True, null=True, choices=DEVICE_GRADE_CHOICES)
#     cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     sku = models.CharField(max_length=255)
#     imei = models.CharField(max_length=15, blank=True, null=True)
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='product_images', blank=True, null=True)
#     defect = models.TextField(blank=True, null=True)
#     url = models.URLField(blank=True, null=True)
#     size = models.CharField(max_length=255, blank=True, null=True)
#     weight = models.CharField(max_length=255, blank=True, null=True)
#     color = models.CharField(max_length=255, blank=True, null=True)
#     sale_start_date = models.DateTimeField(blank=True, null=True)
#     sale_end_date = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.name} - SKU: {self.sku}"
    
#     def is_on_sale(self):
#         return self.sale_start_date <= timezone.now() <= self.sale_end_date
@pytest.mark.django_db
def test_device_model(test_user, test_location, test_supplier):
    device = Device.objects.create(
        owner=test_user('devicetestowner'),
        name='Test Device',
        description='Test Device Description',
        grade='A',
        cost=10.00,
        price=20.00,
        sku='TESTSKU',
        location=test_location,
        supplier=test_supplier,
        imei='123456789012345',
        defect='Test Device Defect',
        url='https://www.testdevice.com',
        size='Test Device Size',
        weight='Test Device Weight',
        color='Test Device Color',
        # sale_start_date=timezone.now(),
        # sale_end_date=timezone.now(),
    )
    assert device.owner.username == 'devicetestowner'
    assert device.name == 'Test Device'
    assert device.description == 'Test Device Description'
    assert device.grade == 'A'
    assert device.cost == 10.00
    assert device.price == 20.00
    assert device.sku == 'TESTSKU'
    assert device.imei == '123456789012345'
    assert device.defect == 'Test Device Defect'
    assert device.url == 'https://www.testdevice.com'
    assert device.size == 'Test Device Size'
    assert device.weight == 'Test Device Weight'
    assert device.color == 'Test Device Color'
    # assert device.sale_start_date == timezone.now()
    # assert device.sale_end_date == timezone.now()
    # assert device.updated_at == timezone.now()
    # assert device.is_on_sale() == False
    assert device.image == None
    assert device.supplier == test_supplier
    assert device.location == test_location
    assert str(device) == 'Test Device - SKU: TESTSKU'

