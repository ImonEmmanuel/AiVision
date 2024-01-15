import pathlib
import PIL
from fastai.learner import load_learner
from fastai.data.all import *
from fastai.vision.all import *
from fastai.vision.core import PILImage
from fastapi import HTTPException, UploadFile


def predict_image():
    pass

def label_func(fname):
    categories = ["Class_"+ str(i) for i in range(1,8)]
    category = fname.parts[-2]  # Extract the category name from the path
    return category if category in labels else "unknown"


temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

labels = ['Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6',
       'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6',
       'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6',
       'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6',
       'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6',
       'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6',
       'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6',
       'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6',
       'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6',
       'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6', 'Class_6',
       'Class_6', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1', 'Class_1',
       'Class_1', 'Class_1', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_2',
       'Class_2', 'Class_2', 'Class_2', 'Class_2', 'Class_5', 'Class_5',
       'Class_5', 'Class_5', 'Class_5', 'Class_5', 'Class_5', 'Class_5',
       'Class_5', 'Class_5', 'Class_5', 'Class_5', 'Class_5', 'Class_5',
       'Class_5', 'Class_5', 'Class_5', 'Class_5', 'Class_5', 'Class_5',
       'Class_5', 'Class_5', 'Class_5', 'Class_5', 'Class_5', 'Class_5',
       'Class_5', 'Class_5', 'Class_5', 'Class_5', 'Class_5', 'Class_7',
       'Class_7', 'Class_7', 'Class_7', 'Class_7', 'Class_7', 'Class_7',
       'Class_7', 'Class_7', 'Class_7', 'Class_7', 'Class_7', 'Class_7',
       'Class_7', 'Class_7', 'Class_7', 'Class_7', 'Class_7', 'Class_7',
       'Class_7', 'Class_7', 'Class_7', 'Class_7', 'Class_4', 'Class_4',
       'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4',
       'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4',
       'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4',
       'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4',
       'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4',
       'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4',
       'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4',
       'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4', 'Class_4',
       'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3',
       'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3',
       'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3',
       'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3',
       'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3',
       'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3',
       'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3',
       'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3',
       'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3',
       'Class_3', 'Class_3', 'Class_3', 'Class_3', 'Class_3']
"""

async def predict_image(file: UploadFile):
    try:
        file_contents = await file.read()
        wound_model = await load_learner(open("trained_model\gpu_densenet169.pkl", "rb"), cpu = True)
        is_cat, _, confidence = await wound_model.predict(file_contents)
        return {
            "prediction" : is_cat,
            "confidence": confidence
        }
    except PIL.UnidentifiedImageError as e:
        raise HTTPException(status_code=400, detail="File is not an image")"""