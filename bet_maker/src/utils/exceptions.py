class AbstractException(Exception):
    detail: str

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
        super().__init__(detail)


class ClientError(AbstractException):
    detail = "Client Response Error"


class RemoteServerError(AbstractException):
    detail = "Error while connecting to remote service"


class UnexpectedError(AbstractException):
    detail = "Unexpected Error"


class ConnectionError(AbstractException):
    detail = "Connection error. Wrong host"
