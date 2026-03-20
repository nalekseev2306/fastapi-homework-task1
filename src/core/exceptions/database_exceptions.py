class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


class NotFoundException(BaseDatabaseException):
    pass


class AlreadyExistsException(BaseDatabaseException):
    pass
