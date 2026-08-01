import allure

from api.order_api import OrderApi


@allure.feature("Заказы")
@allure.story("Получение списка заказов")
class TestOrderList:
    @allure.title("Ответ содержит список заказов")
    def test_get_orders_returns_orders_list(self):
        response = OrderApi.get_list({"limit": 1, "page": 0})

        assert response.status_code == 200
        assert isinstance(response.json().get("orders"), list)
