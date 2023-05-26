from .. import models, schemas 
from fastapi import status, HTTPException, Depends, APIRouter
import requests
from ..settings import config
from sqlalchemy.orm import Session
from ..database import  get_db
from sqlalchemy import and_

router = APIRouter(
    tags=['Account']
)

headers_faceit = {f"Authorization": f"Bearer {config.api_key_faceit.get_secret_value()}"}

@router.post("/account/{faceit_nickname}/", status_code=status.HTTP_201_CREATED)
async def acсount_create(post: schemas.Account, db: Session = Depends(get_db)):
    check = requests.get(f'https://open.faceit.com/data/v4/players?nickname={post.faceit_nickname}', headers=headers_faceit)
    if check.status_code == 404: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'player with nickname {post.faceit_nickname} does not exist')
    else:
        presence = db.query(models.Post).filter(models.Post.telegram_id == post.telegram_id).first()
        if presence:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail=f'player with nickname {post.faceit_nickname} already exists')
        else:
            db.add(models.Post(telegram_id=post.telegram_id, faceit_nickname=post.faceit_nickname))
            db.commit()

@router.put("/update_nickname/{telegram_id}/{new_nick}", status_code=status.HTTP_204_NO_CONTENT)
async def account_update(post: schemas.Account, db: Session = Depends(get_db)):
    check = requests.get(f'https://open.faceit.com/data/v4/players?nickname={post.faceit_nickname}', headers=headers_faceit)
    if check.status_code == 404: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'player with nickname {post.faceit_nickname} does not exist')
    else:
        if db.query(models.Post).filter(and_(models.Post.faceit_nickname == post.faceit_nickname, models.Post.telegram_id == post.telegram_id)).first():
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail=f'player with nickname {post.faceit_nickname} already exists')
        elif not db.query(models.Post).filter(models.Post.telegram_id == post.telegram_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')
        else:
            db.query(models.Post).filter(models.Post.telegram_id == post.telegram_id).update(post.dict(), synchronize_session=False)
            db.commit()

@router.delete('/delete_account/{telegram_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(telegram_id, db: Session = Depends(get_db)):
    if db.query(models.Post).filter(models.Post.telegram_id == telegram_id).first():
        db.query(models.Post).filter(models.Post.telegram_id == telegram_id).delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')