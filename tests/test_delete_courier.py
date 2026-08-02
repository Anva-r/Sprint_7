import allure

from api.courier_api import CourierApi
from data import ResponseMessages, TestData


@allure.feature("Курьеры")
@allure.story("Удаление курьера")
class TestDeleteCourier:
    @allure.title("Курьера можно удалить")
    def test_delete_existing_courier_returns_200_and_ok_true(
        self,
        registered_courier,
    ):
        response = CourierApi.delete(registered_courier.courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Удаление без id возвращает ошибку")
    def test_delete_courier_without_id_returns_400_and_message(self):
        response = CourierApi.delete()

        assert response.status_code == 400
        assert response.json() == ResponseMessages.DELETE_COURIER_MISSING_DATA

    @allure.title("Удаление по несуществующему id возвращает ошибку")
    def test_delete_nonexistent_courier_returns_404_and_message(self):
        response = CourierApi.delete(TestData.NONEXISTENT_ID)

        assert response.status_code == 404
        assert response.json() == ResponseMessages.COURIER_NOT_FOUND
