import pytest
from django.utils import timezone
from store.models import DeviceDefect

@pytest.mark.django_db
def test_create_device_defect():
    defect_name = "Screen Issue"
    description = "The device screen flickers occasionally."
    report = "Reported by multiple users."
    defect_fix = "Replace screen component."
    repair = "Detailed repair procedure."
    notes = "Check screen connector compatibility."
    url = "https://www.example.com/defect/screen-issue"

    defect = DeviceDefect.objects.create(
        defect_name=defect_name,
        description=description,
        report=report,
        defect_fix=defect_fix,
        repair=repair,
        notes=notes,
        url=url
    )

    assert defect.defect_name == defect_name
    assert defect.description == description
    assert defect.report == report
    assert defect.defect_fix == defect_fix
    assert defect.repair == repair
    assert defect.notes == notes
    assert defect.url == url
    assert defect.created_at <= timezone.now()
    assert defect.updated_at <= timezone.now()

@pytest.mark.django_db
def test_device_defect_str():
    defect = DeviceDefect.objects.create(defect_name="Battery Issue")
    assert str(defect) == "Battery Issue"

@pytest.mark.django_db
def test_device_defect_blank_fields():
    defect = DeviceDefect.objects.create(defect_name="Connectivity Problem")
    
    assert defect.description is None
    assert defect.report is None
    assert defect.defect_fix is None
    assert defect.repair is None
    assert defect.notes is None
    assert defect.url is None
