from fastapi import APIRouter, HTTPException, status
import infrastructure.database as dbp
from infrastructure.model import BaseResponseModel, Login, SignUp
import infrastructure.service as ser
from infrastructure.model import BaseResponseModel, SignUp
from auth.authdata import oauth2

router = APIRouter(
    prefix="/authentication",
    tags=["authentication"]
)

@router.post('/SignUp', response_model= BaseResponseModel)
async def create_user(request: SignUp):
    # Check for existing user with the same ID Number
    existing_user = await dbp.check_if_user_exist(request.IdNumber)
    if existing_user:
        raise HTTPException(status_code=400, detail=f"User with Id {request.IdNumber}  already exists")
    # Create the user in the database
    resp = await dbp.create_user(request)

    if resp:
        user_data = {"FirstName":  request.FirstName, "LastName": request.LastName, "IdNumber": request.IdNumber}
        message = "Users retrieved successfully"
        status = True
        return {"data": user_data, "message": message, "status": status}
    else:
        raise HTTPException(status_code=400, detail=f"Error Occured While Creating New User")

@router.post('/Login', response_model= BaseResponseModel)
async def login(request: Login):
    """Handles login requests."""

    # Retrieve user credentials from the request
    id_number = request.IdNumber
    password = request.Password
    
    (resp, user) = await ser.login_check(id_number, password)

    if resp == False:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid credentials")
    
    access_token = oauth2.create_access_token(data = {"sub" : user.IdNumber})

    data = {
        "access_token": access_token,
        "token_type" : "bearer",
        "IdName": user.IdNumber,
        "user" : user
        }
    message = "Login Successful"
    status = True
    return {"data": data, "message": message, "status": status}