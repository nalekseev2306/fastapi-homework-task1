class BaseApiException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail
