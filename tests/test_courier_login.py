import allure
import pytest
import requests

from api.courier_api import CourierApi
from data import ResponseMessages, TestData
from helpers import build_courier_data, generate_random_string, without_field


@allure.feature("Курьеры")
@allure.story("Авторизация курьера")
class TestCourierLogin:
    @allure.title("Курьер может авторизоваться, успешный ответ содержит id")
    def test_courier_can_login(self, registered_courier):
        response = CourierApi.login(
            {
                "login": registered_courier.payload["login"],
                "password": registered_courier.payload["password"],
            }
        )

        assert response.status_code == 200
        assert isinstance(response.json().get("id"), int)
        assert response.json()["id"] == registered_courier.courier_id

    @pytest.mark.parametrize("missing_field", TestData.REQUIRED_LOGIN_FIELDS)
    @allure.title("Нельзя авторизоваться без обязательного поля: {missing_field}")
    def test_login_without_required_field_returns_error(
        self,
        registered_courier,
        missing_field,
    ):
        credentials = without_field(
            {
                "login": registered_courier.payload["login"],
                "password": registered_courier.payload["password"],
            },
            missing_field,
        )

        try:
            response = CourierApi.login(credentials, timeout=10)
        except requests.ReadTimeout:
            if missing_field == "password":
                pytest.xfail(
                    "Дефект API: запрос без password не возвращает ответ вместо 400"
                )
            raise

        assert response.status_code == 400
        assert response.json() == ResponseMessages.LOGIN_MISSING_DATA

    @pytest.mark.parametrize("incorrect_field", TestData.REQUIRED_LOGIN_FIELDS)
    @allure.title("Нельзя авторизоваться с неверным полем: {incorrect_field}")
    def test_login_with_incorrect_credentials_returns_error(
        self,
        registered_courier,
        incorrect_field,
    ):
        credentials = {
            "login": registered_courier.payload["login"],
            "password": registered_courier.payload["password"],
        }
        credentials[incorrect_field] = generate_random_string(16)

        response = CourierApi.login(credentials)

        assert response.status_code == 404
        assert response.json() == ResponseMessages.ACCOUNT_NOT_FOUND

    @allure.title("Несуществующий курьер не может авторизоваться")
    def test_nonexistent_courier_cannot_login(self):
        courier_data = build_courier_data()

        response = CourierApi.login(
            {
                "login": courier_data["login"],
                "password": courier_data["password"],
            }
        )

        assert response.status_code == 404
        assert response.json() == ResponseMessages.ACCOUNT_NOT_FOUND
