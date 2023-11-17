import pytest
from django.utils import timezone
from store.models import Device_IMEI

@pytest.mark.django_db
def test_create_device_imei():
    imei = "123456789012345"
    imei_status = "Active"
    report = "IMEI in good standing."
    url = "https://www.example.com/imei-info"

    device_imei = Device_IMEI.objects.create(
        imei=imei,
        imei_status=imei_status,
        report=report,
        url=url
    )

    assert device_imei.imei == imei
    assert device_imei.imei_status == imei_status
    assert device_imei.report == report
    assert device_imei.url == url
    assert device_imei.created_at <= timezone.now()
    assert device_imei.updated_at <= timezone.now()

@pytest.mark.django_db
def test_device_imei_str():
    imei = "987654321098765"
    device_imei = Device_IMEI.objects.create(imei=imei)
    assert str(device_imei) == imei  # Adjusted to use imei instead of name

@pytest.mark.django_db
def test_device_imei_blank_fields():
    device_imei = Device_IMEI.objects.create()  # No arguments, all fields blank

    assert device_imei.imei is None
    assert device_imei.imei_status is None
    assert device_imei.report is None
    assert device_imei.url is None
