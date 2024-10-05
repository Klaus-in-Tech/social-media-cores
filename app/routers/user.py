from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import database_models, database, schemas, utlis

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session=Depends(database.get_db)):
    # new_user = database_models.Users(email=user.email, password=user.password)
    
    hashed_password = utlis.hash_password(user.password)
    user.password = hashed_password

    new_user = database_models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(database.get_db)):
    # print(id)
    # post = find_post(id)
   
    user = db.query(database_models.Users).filter(database_models.Users.id == id).first()
    print(user)

    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found.")
    return user