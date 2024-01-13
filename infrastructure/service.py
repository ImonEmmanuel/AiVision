import infrastructure.database as dbp
from infrastructure.hash import Hash


async def login_check(Idnumber : str, password : str):
    user = await dbp.get_userinfo(id_number= Idnumber)
    resp = Hash.verify_password(hashed_password=user.Password, plain_password=password) #True Password match
    return (resp, user)

async def generate_session_token():
    """Generates a secure session token."""
    pass
async def set_session_token(token, user_id):
    """Stores the session token in session storage."""
    # Replace with your session storage mechanism
    pass

