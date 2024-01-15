
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from router import authentication, vision, user
from auth import authdata

app = FastAPI(title="AI Vison Backend Version 1")

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

labels = ["Class_1", "Class_2", "Class_3", "Class_4", "Class_5", "Class_6", "Class_7", "Class_8"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "127.0.0.1", port=8000, reload=True)
