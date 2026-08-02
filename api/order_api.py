import allure
import requests

from urls import Urls


class OrderApi:
    TIMEOUT = 60

    @staticmethod
    @allure.step("Создать заказ")
    def create(payload):
        return requests.post(Urls.ORDERS, json=payload, timeout=OrderApi.TIMEOUT)

    @staticmethod
    @allure.step("Получить список заказов")
    def get_list(params=None):
        return requests.get(Urls.ORDERS, params=params, timeout=OrderApi.TIMEOUT)

    @staticmethod
    @allure.step("Принять заказ {order_id} курьером {courier_id}")
    def accept(order_id=None, courier_id=None):
        url = (
            f"{Urls.ORDER_ACCEPT}/{order_id}"
            if order_id is not None
            else f"{Urls.ORDER_ACCEPT}/"
        )
        params = {"courierId": courier_id} if courier_id is not None else None
        return requests.put(url, params=params, timeout=OrderApi.TIMEOUT)

    @staticmethod
    @allure.step("Получить заказ по трек-номеру {track}")
    def get_by_track(track=None):
        params = {"t": track} if track is not None else None
        return requests.get(Urls.ORDER_TRACK, params=params, timeout=OrderApi.TIMEOUT)

    @staticmethod
    @allure.step("Отменить заказ с трек-номером {track}")
    def cancel(track):
        return requests.put(
            Urls.ORDER_CANCEL,
            params={"track": track},
            timeout=OrderApi.TIMEOUT,
        )

    @staticmethod
    @allure.step("Завершить заказ с id={order_id}")
    def finish(order_id):
        return requests.put(
            f"{Urls.ORDER_FINISH}/{order_id}",
            timeout=OrderApi.TIMEOUT,
        )
