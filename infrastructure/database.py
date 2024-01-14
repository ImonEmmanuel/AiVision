from fastapi import HTTPException 
import pypyodbc as odbc
from infrastructure.model import SignUp
from uuid import uuid4
from infrastructure.hash import Hash
from config import SERVER_NAME, DATABASE_NAME, USERNAME, PASSWORD, DRIVER_NAME


connection_string = f"""
        DRIVER={DRIVER_NAME};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        UID={USERNAME};
        PWD={PASSWORD};
"""


# **Helper functions (example implementations):**
async def check_if_user_exist(id_number):
    """Retrieves a user from a hypothetical database."""
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    query = f"""
        SELECT [Id],[Firstname], [Lastname], [Idnumber], [Password]
        FROM [aivision-db].[dbo].[User]
        WHERE [Idnumber] = '{id_number}';            
        """
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.commit()
    cursor.close()
    conn.close()
    if len(data) > 0:  #user exist
        return True
    return False # User does not exist

async def create_user(req : SignUp):
    req.Password = Hash.encrypt(req.Password)
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    query = f"""
            INSERT INTO [aivision-db].[dbo].[User] ([Id], [Firstname], [Lastname], [Idnumber], [Password])
            VALUES 
            ('{uuid4().hex}', '{req.FirstName}', '{req.LastName}', '{req.IdNumber}', '{req.Password}')
            """
    cursor.execute(query)
    cursor.commit()
    cursor.close()
    conn.close()
    return True

async def delete_user(user_id):
    try:
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        # Execute the DELETE query
        query = f"DELETE FROM [aivision-db].[dbo].[newuser] WHERE [Idnumber] = '{user_id}';"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        # Check if any rows were affected
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        
        return {"message": f"User with ID {user_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
    

async def get_userinfo(id_number: str):
    try:
        # Establish a connection and execute the query
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        query = f"""
            SELECT [Firstname], [Lastname], [Idnumber], [Password]
            FROM [aivision-db].[dbo].[User]
            WHERE [Idnumber] = '{id_number}';            
            """
        cursor.execute(query)
        
        # Fetch the first row
        user_data = cursor.fetchone()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Check if the user was found
        if user_data is None:
            raise HTTPException(status_code=404, detail=f"User with ID number {id_number} not found")

        # Map the query result into the Pydantic model
        user_model = SignUp(**dict(zip(SignUp.__annotations__.keys(), user_data)))
        return user_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")