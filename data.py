class ResponseMessages:
    CREATE_COURIER_MISSING_DATA = {
        "code": 400,
        "message": "Недостаточно данных для создания учетной записи",
    }
    COURIER_LOGIN_ALREADY_EXISTS = {
        "code": 409,
        "message": "Этот логин уже используется. Попробуйте другой.",
    }
    LOGIN_MISSING_DATA = {
        "code": 400,
        "message": "Недостаточно данных для входа",
    }
    DELETE_COURIER_MISSING_DATA = {
        "code": 400,
        "message": "Недостаточно данных для удаления курьера",
    }
    ACCOUNT_NOT_FOUND = {"code": 404, "message": "Учетная запись не найдена"}
    COURIER_NOT_FOUND = {"code": 404, "message": "Курьера с таким id нет."}
    ACCEPT_MISSING_DATA = {
        "code": 400,
        "message": "Недостаточно данных для поиска",
    }
    ORDER_ID_NOT_FOUND = {
        "code": 404,
        "message": "Заказа с таким id не существует",
    }
    COURIER_ID_NOT_FOUND = {
        "code": 404,
        "message": "Курьера с таким id не существует",
    }
    TRACK_MISSING = {"code": 400, "message": "Недостаточно данных для поиска"}
    ORDER_NOT_FOUND = {"code": 404, "message": "Заказ не найден"}


class TestData:
    REQUIRED_COURIER_FIELDS = ("login", "password", "firstName")
    REQUIRED_LOGIN_FIELDS = ("login", "password")
    ORDER_COLORS = (
        ("black", {"color": ["BLACK"]}),
        ("grey", {"color": ["GREY"]}),
        ("both", {"color": ["BLACK", "GREY"]}),
        ("without_color", {}),
    )
    NONEXISTENT_ID = 999_999_999
    NONEXISTENT_TRACK = 999_999_999
