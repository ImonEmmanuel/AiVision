from typing import Generic, TypeVar
from pydantic import BaseModel


class SignUp(BaseModel):
    FirstName : str
    LastName : str
    IdNumber : str
    Password : str

class UserModel(BaseModel):
    Id : str
    FirstName : str
    LastName : str
    IdNumber : str

class Login(BaseModel):
    IdNumber : str
    Password : str

class SignUpDisplay(BaseModel):
    FirstName : str
    LastName : str
    IdNumber : str


DataT = TypeVar("DataT")

class BaseResponseModel(BaseModel, Generic[DataT]):
    data: DataT
    message: str
    status: bool