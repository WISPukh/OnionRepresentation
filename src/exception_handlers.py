from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions import BaseError


def handle_exceptions(request: Request, exception: BaseError):  # noqa
    return JSONResponse(
        status_code=exception.status_code, content={
            'error': {
                'details': exception.details
            }
        }
    )
