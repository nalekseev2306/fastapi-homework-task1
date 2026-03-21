class BaseDomainException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class CategoryNotFoundException(BaseDomainException):
    _text_template = "Category with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template)


class CategoryNotFoundBySlugException(BaseDomainException):
    _text_template = "Category with slug '{slug}' not found"

    def __init__(self, slug: int) -> None:
        self._text_template = self._text_template.format(slug=slug)

        super().__init__(detail=self._text_template)


class CategoryWithSlugAlreadyExistException(BaseDomainException):
    _text_template = "Category with slug '{slug}' already exist"

    def __init__(self, slug: int) -> None:
        self._text_template = self._text_template.format(slug=slug)

        super().__init__(detail=self._text_template)


class CommentNotFoundException(BaseDomainException):
    _text_template = "Comment with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template)


class UserNotFoundException(BaseDomainException):
    _text_template = "User with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template)


class PostNotFoundException(BaseDomainException):
    _text_template = "Post with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template)

