from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],
                   responses={404: {"message": "no encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disable: bool
    
    
class UserDB(User):
    password: str
    

users_db = {
    "misael": {
        "username": "misa",
        "fullname": "Misael Terrez",
        "email": "misa.mtj@hotmail.com",
        "disable": False,
        "password": "123456"
    },
    "adriana": {
        "username": "adry",
        "fullname": "Adriana galvez Terrez",
        "email": "adry@hotmail.com",
        "disable": True,
        "password": "78910"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Credenciales de autenticación invalidas", 
                            headers={"WWW-Authenticate": "Bearer"})
        
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Ususario inactivo")
        
        
    return user
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=404, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=404, detail="La constraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}



@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user