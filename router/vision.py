from fastapi import APIRouter, Depends
from auth.oauth2 import get_user_details
from infrastructure.model import BaseResponseModel, SignUp


router = APIRouter(
    prefix="/vision",
    tags=["vision"]
)


@router.post('/UploadImage', response_model= BaseResponseModel)
def upload_image(request: str, current_user : SignUp  = Depends(get_user_details)):
    pass

@router.get('/list_of_available_image', response_model= BaseResponseModel)
def get_available_image(request: str, current_user : SignUp  = Depends(get_user_details)):
    pass