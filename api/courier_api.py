import allure
import requests

from urls import Urls


class CourierApi:
    TIMEOUT = 60

    @staticmethod
    @allure.step("Создать курьера")
    def create(payload):
        return requests.post(Urls.COURIER, json=payload, timeout=CourierApi.TIMEOUT)

    @staticmethod
    @allure.step("Авторизовать курьера")
    def login(payload, timeout=None):
        return requests.post(
            Urls.COURIER_LOGIN,
            json=payload,
            timeout=timeout or CourierApi.TIMEOUT,
        )

    @staticmethod
    @allure.step("Удалить курьера с id={courier_id}")
    def delete(courier_id=None):
        url = f"{Urls.COURIER}/{courier_id}" if courier_id is not None else f"{Urls.COURIER}/"
        return requests.delete(url, timeout=CourierApi.TIMEOUT)
