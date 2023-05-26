from .. import models, schemas 
import requests
import time
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from ..settings import config
from pydantic import parse_obj_as
from app.dictionaries import weapons

router = APIRouter(
    tags=['TRACKERGG API']
)

headers_faceit = {f"Authorization": f"Bearer {config.api_key_faceit.get_secret_value()}"}
headers_tracker = {f"TRN-Api-Key": f"{config.api_key_tracker.get_secret_value()}"}

@router.get("/global_player_csgo_stats/{telegram_id}")
async def get_global_player_csgo_stats_(telegram_id, db: Session = Depends(get_db)):
    teleid = db.query(models.Post).filter(models.Post.telegram_id == telegram_id).first()
    if teleid:
        players = parse_obj_as(schemas.Player, requests.get(f'https://open.faceit.com/data/v4/players?nickname={teleid.faceit_nickname}',
                                                    headers=headers_faceit).json())
        check = requests.get(f'https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{players.steam_id_64}', headers=headers_tracker)
        if check.status_code == 429:
            time.sleep(50)
            check = requests.get(f'https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{players.steam_id_64}', headers=headers_tracker)
        if check.status_code == 451:
            raise HTTPException(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS, detail='Private profile')
        if check.status_code == 400:
            check = requests.get(f'https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{players.steam_id_64}', headers=headers_tracker)
        stats = check.json()
        segments = parse_obj_as(schemas.Model, stats["data"]["segments"][0]["stats"])
        return segments
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')

@router.get("/player_csgo_stats_weapon/{telegram_id}/{weapon_name}")
async def get_player_csgo_stats_weapon_steam_id_64(telegram_id, weapon_name, db: Session = Depends(get_db)):
    teleid = db.query(models.Post).filter(models.Post.telegram_id == telegram_id).first()
    if teleid:
        players = parse_obj_as(schemas.Player, requests.get(f'https://open.faceit.com/data/v4/players?nickname={teleid.faceit_nickname}',
                                                    headers=headers_faceit).json())
        check = requests.get(f'https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{players.steam_id_64}/segments/weapon', headers=headers_tracker)
        if check.status_code == 429:
            time.sleep(50)
            check = requests.get(f'https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{players.steam_id_64}/segments/weapon', headers=headers_tracker)
        if check.status_code == 451:
            raise HTTPException(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS, detail='Private profile')
        if check.status_code == 400:
            check = requests.get(f'https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{players.steam_id_64}/segments/weapon', headers=headers_tracker)
        stats = check.json()
        weapon = parse_obj_as(schemas.Model_Weapon, stats["data"][weapons[f'{weapon_name}'][0]])
        weapon.metadata.imageUrl = weapons[f'{weapon_name}'][1]
        return weapon
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')