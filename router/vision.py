import string
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from auth.oauth2 import get_user_details
from infrastructure.aimodel import predict_image
from infrastructure.model import BaseResponseModel, SignUp
from infrastructure.service import create_image_folder, delete_file, is_image_file


router = APIRouter(
    prefix="/vision",
    tags=["vision"]
)


@router.post('/UploadImage', response_model= BaseResponseModel)
async def upload_image(image: UploadFile = File(...), current_user : SignUp  = Depends(get_user_details)):
    if is_image_file(image.filename):
        message = f"{image.filename} was successfully Uploaded and processing for AI Detection"
        statuss = True
        data = create_image_folder(image)
        #prediction = await predict_image(image)
        _ = delete_file(data['filename'])
        return {"data": data, "message": message, "status": statuss}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{image.filename} is not a valid image file" )

@router.get('/list_of_available_image', response_model= BaseResponseModel)
def get_available_image(request: str, current_user : SignUp  = Depends(get_user_details)):
    pass