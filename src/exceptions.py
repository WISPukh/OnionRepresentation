from typing import Any


class BaseError(Exception):
    def __init__(self, status_code: int, details: Any):
        self.status_code = status_code
        self.details = details


class RemoteServerError(BaseError):
    def __init__(self, details: Any):
        super().__init__(
            status_code=502,
            details=details
        )


class InternalServerError(BaseError):
    def __init__(self, details: Any):
        super().__init__(
            status_code=500,
            details=details
        )
