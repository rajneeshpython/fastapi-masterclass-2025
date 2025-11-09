from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field, BaseModel
from sqlalchemy.orm import Session
from starlette import status

from ..database import SessionLocal
from ..models import User
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerifyRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(User).filter(User.id == user.get('id')).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency, db: db_dependency,
                          user_verify_request: UserVerifyRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(User).filter(User.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verify_request.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_verify_request.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_mode = db.query(User).filter(User.id == user.get('id')).first()
    user_mode.phone_number = phone_number
    db.add(user_mode)
    db.commit()