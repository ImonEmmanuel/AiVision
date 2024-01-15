import string
import PIL
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from auth.oauth2 import get_user_details
from infrastructure.aimodel import predict_image
from infrastructure.model import BaseResponseModel, SignUp
from infrastructure.service import create_image_folder, delete_file, is_image_file


router = APIRouter(
    prefix="/vision",
    tags=["vision"]
)


classes_dict_values = [
    'Abrasions',
    'Bruises',
    'Burns',
    'Cut',
    'Ingrown_nails',
    'Laceration',
    'Stab_wound'
]


@router.get('/list_of_available_image', response_model= BaseResponseModel)
def get_available_image(current_user : SignUp  = Depends(get_user_details)):
    message = f"List of Images"
    statuss = True
    return {"data": classes_dict_values, "message": message, "status": statuss}

@router.post('/UploadImage', response_model= BaseResponseModel)
async def predict_image_test(file: UploadFile, current_user : SignUp  = Depends(get_user_details)):
    try:
        result = await predict_image(file)
        message = f"{file.filename} was successfully Uploaded and processing for AI Detection"
        statuss = True
        return {"data": result, "message": message, "status": statuss}
    
    except PIL.UnidentifiedImageError as e:
        raise HTTPException(status_code=400, detail="An Error Occured while processing Image")