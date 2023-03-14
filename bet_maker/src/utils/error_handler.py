from . import api_exceptions, exceptions


def error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except exceptions.ClientError as e:
            raise api_exceptions.BadRequest(e.detail)
        except exceptions.RemoteServerError as e:
            raise api_exceptions.RemoteServiceError(e.detail)
    return wrapper
