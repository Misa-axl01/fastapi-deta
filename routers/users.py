from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404: {"message": "no encontrado"}})

#inicia el server : uvicorn users:router --reload

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int
    
users_list = [User(id=1, name="Misael",surname="Terrez",url="facebook.com",age="28"),
                User(id=2, name="Adriana",surname="Galvez",url="facebook.com",age="24")]
    

@router.get("/usersjson")
async def usersjson():
    return [{"id": "1", "name": "Misael", "surname": "Terrez", "url": "facebook.com", "age": "28"},
            {"id": "2","name": "Adriana", "surname": "Galvez", "url": "facebook.com", "age": "24"}]
    
@router.get("/users")
async def users():
    return users_list

#@router.get("/user/{id}")
#async def userid(id: int):
#    users = filter(lambda user: user.id == id, users_list)
#    try:
#        return list(users)[0]
#    except:
#        return {"error":"no ser ha encontrado el usuario"}

@router.get("/userq/")
async def userid(id: int):
    return search_user(id)
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no ser ha encontrado el usuario"}
    
@router.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "el ususario ya existe"}
    else:
        users_list.routerend(user)
        return user 
        
@router.put("/user/")
async def user(user: User):
    
    found = False
    
    for index, save_user in enumerate(users_list):
        if save_user.id == user.id:
            users_list[index] = user
            found = True
            
    if not found:
        return {"error": "no se ha actualizado el usuario"}
    else:
        return user
    
@router.delete("/user/{id}")
async def userid(id: int):
    found = False  

    for index, save_user in enumerate(users_list):
        if save_user.id == id:
            del users_list[index]
            found = True
            
        if not found:
            return {"error": "no se ha eliminado el usuario"}