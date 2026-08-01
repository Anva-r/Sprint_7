import allure
import pytest

from api.courier_api import CourierApi
from data import ResponseMessages, TestData
from helpers import build_courier_data, without_field


@allure.feature("Курьеры")
@allure.story("Создание курьера")
class TestCreateCourier:
    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, courier_factory):
        courier = courier_factory()

        assert courier.response.status_code == 201
        assert courier.response.json() == {"ok": True}

    @allure.title("Нельзя создать двух курьеров с одинаковым логином")
    def test_create_duplicate_courier_returns_conflict(self, courier_factory):
        courier_data = build_courier_data()
        first_response = courier_factory(courier_data).response
        second_response = CourierApi.create(courier_data)

        assert first_response.status_code == 201
        assert first_response.json() == {"ok": True}
        assert second_response.status_code == 409
        assert second_response.json() == ResponseMessages.COURIER_LOGIN_ALREADY_EXISTS

    @pytest.mark.parametrize("missing_field", TestData.REQUIRED_COURIER_FIELDS)
    @allure.title("Нельзя создать курьера без обязательного поля: {missing_field}")
    def test_create_courier_without_required_field_returns_error(self, missing_field):
        payload = without_field(build_courier_data(), missing_field)

        response = CourierApi.create(payload)

        assert response.status_code == 400
        assert response.json() == ResponseMessages.CREATE_COURIER_MISSING_DATA
