from dataclasses import dataclass

import allure
import pytest

from api.courier_api import CourierApi
from api.order_api import OrderApi
from helpers import build_courier_data, build_order_data


@dataclass
class CourierRecord:
    payload: dict
    courier_id: int
    response: object


@dataclass
class OrderRecord:
    payload: dict
    track: int
    order_id: int
    response: object


@pytest.fixture
def courier_factory():
    created_courier_ids = []

    def create_courier(payload=None):
        courier_payload = payload or build_courier_data()
        response = CourierApi.create(courier_payload)
        courier_id = None

        if response.status_code == 201:
            login_response = CourierApi.login(
                {
                    "login": courier_payload["login"],
                    "password": courier_payload["password"],
                }
            )
            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                created_courier_ids.append(courier_id)

        return CourierRecord(courier_payload, courier_id, response)

    yield create_courier

    for courier_id in reversed(created_courier_ids):
        with allure.step(f"Очистить курьера с id={courier_id}"):
            cleanup_response = CourierApi.delete(courier_id)
            assert cleanup_response.status_code in (200, 404), (
                f"Не удалось удалить курьера {courier_id}: "
                f"{cleanup_response.status_code} {cleanup_response.text}"
            )


@pytest.fixture
def registered_courier(courier_factory):
    courier = courier_factory()
    assert courier.response.status_code == 201, (
        "Не удалось подготовить курьера: "
        f"{courier.response.status_code} {courier.response.text}"
    )
    assert courier.courier_id is not None, "API не вернул id подготовленного курьера"
    return courier


@pytest.fixture
def order_factory():
    created_orders = []

    def create_order(payload=None):
        order_payload = payload or build_order_data()
        response = OrderApi.create(order_payload)
        track = None
        order_id = None

        if response.status_code == 201:
            track = response.json()["track"]
            track_response = OrderApi.get_by_track(track)
            if track_response.status_code == 200:
                order_id = track_response.json()["order"]["id"]
            created_orders.append((track, order_id))

        return OrderRecord(order_payload, track, order_id, response)

    yield create_order

    for track, order_id in reversed(created_orders):
        with allure.step(f"Очистить заказ с трек-номером {track}"):
            cancel_response = OrderApi.cancel(track)
            if cancel_response.status_code == 200:
                assert cancel_response.json() == {"ok": True}
            elif cancel_response.status_code == 409 and order_id is not None:
                finish_response = OrderApi.finish(order_id)
                assert finish_response.status_code == 200, (
                    f"Не удалось завершить принятый заказ {order_id}: "
                    f"{finish_response.status_code} {finish_response.text}"
                )
                assert finish_response.json() == {"ok": True}
            else:
                pytest.fail(
                    f"Не удалось очистить заказ {track}: "
                    f"{cancel_response.status_code} {cancel_response.text}"
                )


@pytest.fixture
def created_order(order_factory):
    order = order_factory()
    assert order.response.status_code == 201, (
        "Не удалось подготовить заказ: "
        f"{order.response.status_code} {order.response.text}"
    )
    assert order.order_id is not None, "API не вернул id подготовленного заказа"
    return order
