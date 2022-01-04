from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from starlette.status import HTTP_404_NOT_FOUND

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')

    # create and return a token since user is valid
    access_token = oauth2.create_token(data={"user_id": user.id})
    return {"accesS_token": access_token, "token_type": "bearer"}
