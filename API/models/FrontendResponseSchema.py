from pydantic import BaseModel

from typing import List
class FrontendResponseModel(BaseModel):
    status:str
    message: List[str]
    data:dict

    