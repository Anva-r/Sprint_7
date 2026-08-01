import allure
import pytest

from data import TestData
from helpers import build_order_data


@allure.feature("Заказы")
@allure.story("Создание заказа")
class TestCreateOrder:
    @pytest.mark.parametrize(
        ("case_name", "colors"),
        TestData.ORDER_COLORS,
        ids=[case[0] for case in TestData.ORDER_COLORS],
    )
    @allure.title("Заказ можно создать с вариантом цвета: {case_name}")
    def test_create_order_with_color_options_returns_track(
        self,
        order_factory,
        case_name,
        colors,
    ):
        payload = build_order_data()
        if colors is not None:
            payload["color"] = colors

        order = order_factory(payload)

        assert order.response.status_code == 201
        assert isinstance(order.response.json().get("track"), int)
