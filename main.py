from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import infrastructure.database as dbp
from infrastructure.model import BaseResponseModel
from router import authentication, vision, user
from auth import authdata

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





