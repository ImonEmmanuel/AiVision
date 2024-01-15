import pathlib
import PIL
from click import File
from fastapi import Depends, FastAPI, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from auth.oauth2 import get_user_details
import infrastructure.database as dbp
from infrastructure.model import BaseResponseModel, SignUp
from infrastructure.service import create_image_folder, delete_file, is_image_file
from router import authentication, vision, user
from auth import authdata
from fastai.learner import load_learner

app = FastAPI()

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authdata.router)
app.include_router(authentication.router)
app.include_router(vision.router)
app.include_router(user.router)

app.mount("/images", StaticFiles(directory ="images"), name="images")


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


@app.post("/upload_image")
async def predict_image(file: UploadFile):
    try:
        file_contents = await file.read()
        wound_model = load_learner(open("trained_model\gpu_densenet169.pkl", "rb"), cpu = True)
        is_cat, _, confidence = wound_model.predict(file_contents)
        return {
            "prediction" : is_cat,
            "confidence": confidence
        }
    except PIL.UnidentifiedImageError as e:
        raise HTTPException(status_code=400, detail="File is not an image")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "127.0.0.1", port=8000, reload=True, workers=2)
