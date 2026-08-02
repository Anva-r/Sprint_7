import allure
import pytest

from api.order_api import OrderApi
from data import TestData
from helpers import build_order_data


@allure.feature("Заказы")
@allure.story("Создание заказа")
class TestCreateOrder:
    @pytest.mark.parametrize(
        ("case_name", "color_data"),
        TestData.ORDER_COLORS,
        ids=[case[0] for case in TestData.ORDER_COLORS],
    )
    @allure.title("Заказ можно создать с вариантом цвета: {case_name}")
    def test_create_order_with_color_options_returns_201_and_track(
        self,
        order_cleanup,
        case_name,
        color_data,
    ):
        payload = build_order_data()
        payload.update(color_data)
        response = OrderApi.create(payload)
        track = response.json().get("track")
        order_cleanup.append(track)

        assert response.status_code == 201
        assert isinstance(track, int)
