from copy import deepcopy
from datetime import date, timedelta
from uuid import uuid4


def generate_random_string(length=10):
    return uuid4().hex[:length]


def build_courier_data():
    suffix = generate_random_string()
    return {
        "login": f"courier_{suffix}",
        "password": generate_random_string(12),
        "firstName": f"name_{suffix}",
    }


def build_order_data():
    suffix = generate_random_string(8)
    return {
        "firstName": f"Test{suffix}",
        "lastName": "CourierApi",
        "address": "Москва, Тестовая улица, 1",
        "metroStation": 4,
        "phone": "+7 999 000 00 00",
        "rentTime": 2,
        "deliveryDate": (date.today() + timedelta(days=2)).isoformat(),
        "comment": f"autotest-{suffix}",
    }


def without_field(payload, field):
    changed_payload = deepcopy(payload)
    changed_payload.pop(field, None)
    return changed_payload
