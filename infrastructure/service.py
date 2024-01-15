import random
import shutil
import string
from click import File
from fastapi import UploadFile
import infrastructure.database as dbp
from infrastructure.hash import Hash
import os


async def login_check(Idnumber : str, password : str):
    user = await dbp.get_userinfo(id_number= Idnumber)
    resp = Hash.verify_password(hashed_password=user.Password, plain_password=password) #True Password match
    return (resp, user)

def is_image_file(filename):
    image_extensions = ['jpg', 'jpeg', 'png', 'gif','tiff']
    # Get the file extension from the filename
    file_extension = filename.lower().split('.')[-1]
    # Check if the file extension is in the list of image extensions
    return file_extension in image_extensions

def create_image_folder(image_data: UploadFile = File(...)):
    letters = string.ascii_letters
    rand_Str = "".join(random.choice(letters) for i in range(8))
    ext = image_data.filename.lower().split('.')[-1]
    file = f"{rand_Str}.{ext}"
    path = f'images/{file}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image_data.file, buffer)
    return {"filename": path}

def delete_file(file_path: str):
    try:
        os.remove(file_path)
        return {"message": f"File {file_path} deleted successfully"}
    except FileNotFoundError:
        return {"error": f"File {file_path} not found"}
