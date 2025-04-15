from http import HTTPStatus


class AppException(Exception):
    """
    Базовое приложение-специфичное исключение.

    :param message: Сообщение об ошибке.
    :param code: HTTP статус-код (по умолчанию 400 Bad Request).
    :param detail: Детализированное описание ошибки (если не указано — будет использоваться message).
    """

    def __init__(self, message, code=HTTPStatus.BAD_REQUEST, detail: str | None = None):
        self.message = message
        self.code = code
        self.detail = detail or self.message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.detail}'

    def __repr__(self):
        return f'{self.__class__.__name__}(code={self.code}, detail={self.detail})'


class EntityNotFoundError(AppException):
    """Исключение, выбрасываемое при отсутствии сущности в базе данных."""

    def __init__(self, entity_name: str, entity_id: str | int):
        super().__init__(
            message=f"{entity_name} с идентификатором '{entity_id}' не найден.",
            code=HTTPStatus.NOT_FOUND
        )


class EntityAlreadyExistsError(AppException):
    """Исключение, выбрасываемое при попытке создать уже существующую сущность."""

    def __init__(self, entity_name: str):
        super().__init__(
            message=f"{entity_name} с такими данными уже существует.",
            code=HTTPStatus.CONFLICT
        )


class ReservationConflictError(AppException):
    """Исключение, выбрасываемое при попытке забронировать занятый столик."""

    def __init__(self, table_id: int | str):
        super().__init__(
            message=f'Столик с id {table_id} уже забронирован на указанное время.',
            code=HTTPStatus.CONFLICT
        )
