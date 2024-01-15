import pathlib
import PIL
from fastai.learner import load_learner
from fastai.data.all import *
from fastai.vision.all import *
from fastai.vision.core import PILImage
from fastapi import HTTPException, UploadFile


temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

classes_dict = {
    'Class_1': 'Abrasions',
    'Class_2': 'Bruises',
    'Class_3': 'Burns',
    'Class_4': 'Cut',
    'Class_5': 'Ingrown_nails',
    'Class_6': 'Laceration',
    'Class_7': 'Stab_wound'
}

async def predict_image(file: UploadFile):
    try:
        file_contents = await file.read()
        wound_model = load_learner(open("trained_model\gpu_densenet169.pkl", "rb"), cpu = True)
        is_cat, _, confidence = wound_model.predict(file_contents)
        return {
            "prediction" : classes_dict[is_cat],
        }
    
    except PIL.UnidentifiedImageError as e:
        raise HTTPException(status_code=400, detail="File is not an image")