class Urls:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    API_V1 = f"{BASE_URL}/api/v1"

    COURIER = f"{API_V1}/courier"
    COURIER_LOGIN = f"{COURIER}/login"

    ORDERS = f"{API_V1}/orders"
    ORDER_ACCEPT = f"{ORDERS}/accept"
    ORDER_CANCEL = f"{ORDERS}/cancel"
    ORDER_FINISH = f"{ORDERS}/finish"
    ORDER_TRACK = f"{ORDERS}/track"
