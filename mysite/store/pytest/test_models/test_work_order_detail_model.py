# class WorkOrderDetail(models.Model):
#     work_order = models.ForeignKey(WorkOrder, related_name='details', on_delete=models.CASCADE)
#     service_detail = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE)
#     part= models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # @property
#     # def quantity_changed(self):
#     #     return self.quantity != self.quantity
    
#     def __str__(self):
#         return f"Work Order {self.work_order.id} Detail - Part: 'N/A'"


import pytest
from decimal import Decimal
from django.utils import timezone
from store.models import WorkOrderDetail

@pytest.mark.django_db
def test_work_order_detail_model(test_work_order, test_service_detail, test_part):
    work_order_detail = WorkOrderDetail.objects.create(
        work_order=test_work_order,
        service_detail=test_service_detail,
        part=test_part,
    )
    assert work_order_detail.work_order == test_work_order
    assert work_order_detail.service_detail == test_service_detail
    assert work_order_detail.created_at <= timezone.now()
    assert work_order_detail.updated_at <= timezone.now()
    assert work_order_detail.part == test_part
    assert str(work_order_detail) == f"Work Order {test_work_order.id} Detail - Part: 'N/A'"
