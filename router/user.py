from fastapi import APIRouter, Depends
import infrastructure.database as dbp
from infrastructure.model import BaseResponseModel, SignUp
from auth.oauth2 import get_user_details, oauth2_schema

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.delete("/delete/{id_number}", response_model= BaseResponseModel)
async def delete_user(id_number: str, current_user : SignUp  = Depends(get_user_details)):
    resp = await dbp.delete_user(id_number)
    message = f"Users with IdNumber {id_number} successfully deleted "
    status = True
    return {"data": resp, "message": message, "status": status}


@router.get("/get_user/{id_number}", response_model=BaseResponseModel)
async def get_user(id_number : str, current_user : SignUp  = Depends(get_user_details)):
    resp = await dbp.get_userinfo(id_number = id_number)
    message = "Success"
    status = True
    return {"data": resp, "message": message, "status": status}

@router.get("/get_user_info", response_model=BaseResponseModel)
async def get_user_info(current_user : SignUp  = Depends(get_user_details)):
    resp = await dbp.get_userinfo(id_number = current_user.IdNumber)
    message = "Success"
    status = True
    return {"data": resp, "message": message, "status": status}



@router.get("/get_all_user", response_model=BaseResponseModel)
async def get_all_user(current_user : SignUp  = Depends(get_user_details)):
    resp = await dbp.get_all_user()
    message = "Success"
    status = True
    return {"data": resp, "message": message, "status": status}