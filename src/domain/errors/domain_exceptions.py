class DomainException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class UserNotFoundError(DomainException):
    def __init__(self, message: str = 'User not found'):
        super().__init__(message)


class UserAlreadyExistsError(DomainException):
    def __init__(self, message: str = 'User already exists'):
        super().__init__(message)


class InvalidPageError(DomainException):
    def __init__(self, message: str = 'Invalid page'):
        super().__init__(message)


class InvalidPageSizeError(DomainException):
    def __init__(self, message: str = 'Invalid page size'):
        super().__init__(message)
