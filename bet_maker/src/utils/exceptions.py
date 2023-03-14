class AbstractException(Exception):
    detail: str

    def __init__(self, exc_info: str, msg: str | None = None):
        if msg is not None:
            self.detail = msg
        self.exc_info = exc_info
        self.args = (self.exc_info,)

    def __str__(self) -> str:
        return f"{self.detail}. Args = {self.args}"


class ClientError(AbstractException):
    detail = "Client Response Error"


class RemoteServerError(AbstractException):
    detail = "Error while connecting to remote service"


class UnexpectedError(AbstractException):
    detail = "Unexpected Error"


class ConnectionError(AbstractException):
    detail = "Connection error. Wrong host"