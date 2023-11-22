# class ServiceDetail(models.Model):
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     part = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True)
#     service_description = models.TextField(default='repair')
#     part_cost = models.DecimalField(max_digits=10, decimal_places=2, default=888.88)
#     service_cost = models.DecimalField(max_digits=10, decimal_places=2, default=888.88)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def service_price(self):
#         return self.service_cost + self.part_cost

#     def __str__(self):
#         return f"Detail for Service {self.service.name}"


import pytest
from decimal import Decimal
from django.utils import timezone
from store.models import ServiceDetail


@pytest.mark.django_db
def test_service_detail_model(test_service, test_part):
    service_detail = ServiceDetail.objects.create(
        service=test_service,
        # part=test_part,
        service_description='Test service description',
        part_cost=Decimal('100.00'),
        service_cost=Decimal('100.00'),
    )
    assert service_detail.service == test_service
    # assert service_detail.part == test_part
    assert service_detail.service_description == 'Test service description'
    assert service_detail.part_cost == Decimal('100.00')
    assert service_detail.service_cost == Decimal('100.00')
    assert service_detail.created_at
    assert service_detail.updated_at
    assert str(service_detail) == f"Detail for Service {test_service.name}"
    assert service_detail.service_price() == Decimal('200.00')