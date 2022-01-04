from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils
from starlette.status import HTTP_404_NOT_FOUND

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')

    # create and return a token since user is valid
    return{'token': 'eample token'}
