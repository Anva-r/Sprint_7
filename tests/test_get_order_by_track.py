import allure

from api.order_api import OrderApi
from data import ResponseMessages, TestData


@allure.feature("Заказы")
@allure.story("Получение заказа по трек-номеру")
class TestGetOrderByTrack:
    @allure.title("По существующему трек-номеру возвращается объект заказа")
    def test_get_order_by_existing_track_returns_200_and_order(self, created_order):
        response = OrderApi.get_by_track(created_order.track)

        assert response.status_code == 200
        assert isinstance(response.json().get("order"), dict)
        assert response.json()["order"]["track"] == created_order.track

    @allure.title("Запрос без трек-номера возвращает ошибку")
    def test_get_order_without_track_returns_400_and_message(self):
        response = OrderApi.get_by_track()

        assert response.status_code == 400
        assert response.json() == ResponseMessages.TRACK_MISSING

    @allure.title("Несуществующий трек-номер возвращает ошибку")
    def test_get_order_by_nonexistent_track_returns_404_and_message(self):
        response = OrderApi.get_by_track(TestData.NONEXISTENT_TRACK)

        assert response.status_code == 404
        assert response.json() == ResponseMessages.ORDER_NOT_FOUND
