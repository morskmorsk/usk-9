# class Service(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
#     technician = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     service_date = models.DateTimeField(auto_now_add=True)


#     def __str__(self):
#         return self.name

import pytest
from store.models import Service
from django.utils import timezone


# create test for service model
@pytest.mark.django_db
def test_service_creation(test_work_order, new_user_profile, test_time):
    name = 'Test Service'
    description = 'Test Description'
    work_order = test_work_order
    technician = new_user_profile('testtechnician')
    service_date = test_time
    service = Service.objects.create(
        name=name,
        description=description,
        work_order=work_order,
        technician=technician,
        service_date=service_date,
    )
    assert service.id == 1
    assert service.name == 'Test Service'
    assert service.description == 'Test Description'
    assert service.work_order == work_order
    assert service.technician == technician
    # assert service.service_date == service_date
    assert str(service) == service.name