from fastapi import status
from fastapi.exceptions import HTTPException


class AbstractHTTPException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail: str

    def __init__(
            self,
            detail: str | None = None,
            headers: dict | None = None,
        ):
        if detail:
            self.detail = detail
        super().__init__(self.status_code, self.detail, headers)


class BadRequest(AbstractHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Bad Request'


class RemoteServiceError(AbstractHTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Remote Service Error'


class ServerError(AbstractHTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Server Error'
