from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import service as ser
from auth import oauth2

from model import Login

router = APIRouter(
    tags = ['authdata']
)

@router.post('/token')
async def get_token(request : OAuth2PasswordRequestForm = Depends()):
    # Retrieve user credentials from the request
    id_number = request.username
    password = request.password
    
    (resp, user) = await ser.login_check(id_number, password)

    if resp == False:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid credentials")
    
    access_token = oauth2.create_access_token(data = {"sub" : user.IdNumber})

    return {
        "access_token": access_token,
        "token_type" : "bearer",
        "IdName": user.IdNumber,
        "firstName": user.FirstName,
        "LastName" : user.LastName
    }
