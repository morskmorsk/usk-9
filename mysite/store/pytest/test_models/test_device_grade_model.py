import pytest
from django.utils import timezone
from store.models import DeviceGrade

@pytest.mark.django_db
def test_create_device_grade():
    grade_name = "Premium"
    description = "Top-tier quality and performance."

    grade = DeviceGrade.objects.create(
        name=grade_name,
        description=description
    )

    assert grade.name == grade_name
    assert grade.description == description
    assert grade.created_at <= timezone.now()
    assert grade.updated_at <= timezone.now()

@pytest.mark.django_db
def test_device_grade_str():
    grade = DeviceGrade.objects.create(name="Standard")
    assert str(grade) == "Standard"

@pytest.mark.django_db
def test_device_grade_blank_fields():
    grade = DeviceGrade.objects.create(name="Economy")
    
    assert grade.description is None
