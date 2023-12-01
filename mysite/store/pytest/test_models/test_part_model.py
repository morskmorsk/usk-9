# class Part(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
#     quantity_available = models.IntegerField(default=0)
#     quantity_reserved = models.IntegerField(default=0)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     sku = models.CharField(max_length=255)
#     url = models.URLField(blank=True, null=True)
#     image = models.ImageField(upload_to='product_images', blank=True, null=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

import pytest
from store.models import Part
from django.utils import timezone

@pytest.mark.django_db
def test_part_creation(test_supplier, test_location, test_department):
    name = 'Test Part'
    description = 'Test Description'
    department = test_department
    location = test_location
    supplier = test_supplier
    quantity_available = 100
    quantity_reserved = 0
    price = 100.00
    sku = 'TESTSKU'
    url = 'https://www.testpart.com'
    part = Part.objects.create(
        name=name,
        description=description,
        department=department,
        location=location,
        supplier=supplier,
        quantity_available=quantity_available,
        quantity_reserved=quantity_reserved,
        price=price,
        sku=sku,
        url=url,
    )
    assert part.id == 1
    assert part.name == 'Test Part'
    assert part.description == 'Test Description'
    assert part.department == department
    assert part.location == location
    assert part.supplier == supplier
    assert part.quantity_available == quantity_available
    assert part.quantity_reserved == quantity_reserved
    assert part.price == price
    assert part.sku == sku
    assert part.url == url
    assert str(part) == part.name
