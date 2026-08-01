import allure

from api.order_api import OrderApi
from data import ResponseMessages, TestData


@allure.feature("Заказы")
@allure.story("Принятие заказа")
class TestAcceptOrder:
    @allure.title("Курьер может принять заказ")
    def test_accept_order_success(self, registered_courier, created_order):
        response = OrderApi.accept(
            created_order.order_id,
            registered_courier.courier_id,
        )

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Нельзя принять заказ без id курьера")
    def test_accept_order_without_courier_id_returns_error(self, created_order):
        response = OrderApi.accept(order_id=created_order.order_id)

        assert response.status_code == 400
        assert response.json() == ResponseMessages.ACCEPT_MISSING_DATA

    @allure.title("Нельзя принять заказ с несуществующим id курьера")
    def test_accept_order_with_nonexistent_courier_id_returns_error(self, created_order):
        response = OrderApi.accept(
            created_order.order_id,
            TestData.NONEXISTENT_ID,
        )

        assert response.status_code == 404
        assert response.json() == ResponseMessages.COURIER_ID_NOT_FOUND

    @allure.title("Нельзя принять заказ без id заказа")
    def test_accept_order_without_order_id_returns_error(self, registered_courier):
        response = OrderApi.accept(courier_id=registered_courier.courier_id)

        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Not Found."}

    @allure.title("Нельзя принять заказ с несуществующим id заказа")
    def test_accept_order_with_nonexistent_order_id_returns_error(
        self,
        registered_courier,
    ):
        response = OrderApi.accept(
            TestData.NONEXISTENT_ID,
            registered_courier.courier_id,
        )

        assert response.status_code == 404
        assert response.json() == ResponseMessages.ORDER_ID_NOT_FOUND
