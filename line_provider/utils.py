import pydantic
from fastapi.responses import JSONResponse


class MyResponse(JSONResponse):
    def __init__(self, data: pydantic.BaseModel, errors: list[str] = []):
        content = {'data': data, 'errors': errors}
        super().__init__(content)