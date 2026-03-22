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

    def __init__(self, slug: str) -> None:
        self._text_template = self._text_template.format(slug=slug)

        super().__init__(detail=self._text_template)


class CategoryWithSlugAlreadyExistException(BaseDomainException):
    _text_template = "Category with slug '{slug}' already exist"

    def __init__(self, slug: str) -> None:
        self._text_template = self._text_template.format(slug=slug)

        super().__init__(detail=self._text_template)


class CommentNotFoundException(BaseDomainException):
    _text_template = "Comment with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template)


class LocationNotFoundException(BaseDomainException):
    _text_template = "Location with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template)


class LocationNotFoundByNameException(BaseDomainException):
    _text_template = "Location with name '{name}' not found"

    def __init__(self, name: str) -> None:
        self._text_template = self._text_template.format(name=name)

        super().__init__(detail=self._text_template)


class LocationWithNameAlreadyExistException(BaseDomainException):
    _text_template = "Location with name '{name}' already exist"

    def __init__(self, name: str) -> None:
        self._text_template = self._text_template.format(name=name)

        super().__init__(detail=self._text_template)


class UserNotFoundException(BaseDomainException):
    _text_template = "User with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template)

class UserNotFoundByUsernameException(BaseDomainException):
    _text_template = "User with username '{username}' not found"

    def __init__(self, username: str) -> None:
        self._text_template = self._text_template.format(username=username)

        super().__init__(detail=self._text_template)
        

class UserNotFoundByEmailException(BaseDomainException):
    _text_template = "User with email '{email}' not found"

    def __init__(self, email: str) -> None:
        self._text_template = self._text_template.format(email=email)

        super().__init__(detail=self._text_template)


class UserWithUsernameAlreadyExistException(BaseDomainException):
    _text_template = "User with username '{username}' already exist"

    def __init__(self, username: str) -> None:
        self._text_template = self._text_template.format(username=username)

        super().__init__(detail=self._text_template)


class UserWithEmailAlreadyExistException(BaseDomainException):
    _text_template = "User with email '{email}' already exist"

    def __init__(self, email: str) -> None:
        self._text_template = self._text_template.format(email=email)

        super().__init__(detail=self._text_template)


class PostNotFoundException(BaseDomainException):
    _text_template = "Post with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template)

