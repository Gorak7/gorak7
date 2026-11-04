from pydantic import BaseModel,Field
from typing import Literal
class GeneratedTestCase(BaseModel):
    name:str=Field(min_length=3,max_length=160)
    operation_id:str
    method:Literal["GET","POST","PUT","PATCH","DELETE"]
    path:str
    expected_status:int=Field(ge=100,le=599)
    category:Literal["positive","negative","boundary","auth"]
    rationale:str=Field(min_length=5,max_length=500)
    headers:dict[str,str]=Field(default_factory=dict)
    body:dict|None=None
