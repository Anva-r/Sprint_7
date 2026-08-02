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


@dataclass
class OrderRecord:
    track: int
    order_id: int


@pytest.fixture
def courier_cleanup():
    created_couriers = []

    yield created_couriers

    for payload, status_code in reversed(created_couriers):
        if status_code != 201:
            continue

        login_response = CourierApi.login(
            {
                "login": payload["login"],
                "password": payload["password"],
            }
        )
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            with allure.step(f"Удалить тестового курьера с id={courier_id}"):
                CourierApi.delete(courier_id)


@pytest.fixture
def registered_courier():
    payload = build_courier_data()
    CourierApi.create(payload)
    login_response = CourierApi.login(
        {
            "login": payload["login"],
            "password": payload["password"],
        }
    )
    courier = CourierRecord(payload, login_response.json()["id"])

    yield courier

    with allure.step(f"Удалить тестового курьера с id={courier.courier_id}"):
        CourierApi.delete(courier.courier_id)


@pytest.fixture
def order_cleanup():
    created_order_tracks = []

    yield created_order_tracks

    for track in reversed(created_order_tracks):
        if track is not None:
            with allure.step(f"Отменить тестовый заказ с трек-номером {track}"):
                OrderApi.cancel(track)


@pytest.fixture
def created_order():
    response = OrderApi.create(build_order_data())
    track = response.json()["track"]
    track_response = OrderApi.get_by_track(track)
    order = OrderRecord(track, track_response.json()["order"]["id"])

    yield order

    with allure.step(f"Очистить заказ с трек-номером {order.track}"):
        cancel_response = OrderApi.cancel(order.track)
        if cancel_response.status_code == 409:
            OrderApi.finish(order.order_id)
