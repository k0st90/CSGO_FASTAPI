from .. import models, schemas 
import requests
from ..settings import config
from sqlalchemy.orm import Session
from ..database import  get_db
from fastapi import status, HTTPException, Depends, APIRouter
from pydantic import parse_obj_as
from datetime import datetime
from app.dictionaries import maps

router = APIRouter(
    tags=['Faceit API']
)


headers_faceit = {f"Authorization": f"Bearer {config.api_key_faceit.get_secret_value()}"}

@router.get("/player_details_by_nickname/{telegram_id}")
async def get_player_details_nick_faceit(telegram_id: int, db: Session = Depends(get_db)):
    teleid = db.query(models.Post).filter(models.Post.telegram_id == telegram_id)
    tel = teleid.first()
    if tel:
        players = parse_obj_as(schemas.Player, requests.get(f'https://open.faceit.com/data/v4/players?nickname={tel.faceit_nickname}',
                                               headers=headers_faceit).json())
        teleid.update({"search_count": tel.search_count+1}, synchronize_session=False)
        db.commit()
        players.search_count = tel.search_count
        return players
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')
    
@router.get("/player_friendsids_by_nickname/{telegram_id}")
async def get_player_friends_nick_faceit(telegram_id: int, db: Session = Depends(get_db)):
    teleid = db.query(models.Post).filter(models.Post.telegram_id == telegram_id).first()
    if teleid:
        friends = parse_obj_as(schemas.Player, requests.get(f'https://open.faceit.com/data/v4/players?nickname={teleid.faceit_nickname}',
                                                 headers=headers_faceit).json())
        friend = []
        for i in range(len(friends.friends_ids)):
            try:
                players = parse_obj_as(schemas.Player, requests.get(f'https://open.faceit.com/data/v4/players/{friends.friends_ids[i]}',
                                                    headers=headers_faceit).json())
                link = f'https://www.faceit.com/{players.settings.language}/players/{players.nickname}'
                friend.append(f'<a href="{link}">{players.nickname}</a>')
            except  Exception as error:
                pass
        return friend
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')
    
@router.get("/player_extended_csgo_stats/{telegram_id}")
async def player_extended_csgo_stats(telegram_id, db: Session = Depends(get_db)):
    teleid = db.query(models.Post).filter(models.Post.telegram_id == telegram_id).first()
    if teleid:
        players = parse_obj_as(schemas.Player, requests.get(f'https://open.faceit.com/data/v4/players?nickname={teleid.faceit_nickname}',
                                                headers=headers_faceit).json())
        stats = parse_obj_as(schemas.Stats, requests.get(f'https://open.faceit.com/data/v4/players/{players.player_id}/stats/csgo',
                                             headers=headers_faceit).json())
        stats.lifetime.recent_results = ['W' if item == '1' else 'L' for item in stats.lifetime.recent_results]
        return stats
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')

@router.get("/player_map_csgo_stats/{map_name}/{telegram_id}")
async def player_map_csgo_stats(telegram_id, map_name, db: Session = Depends(get_db)):
    teleid = db.query(models.Post).filter(models.Post.telegram_id == telegram_id).first()
    if teleid:
        players = parse_obj_as(schemas.Player, requests.get(f'https://open.faceit.com/data/v4/players?nickname={teleid.faceit_nickname}',
                                                headers=headers_faceit).json())
        player = requests.get(f'https://open.faceit.com/data/v4/players/{players.player_id}/stats/csgo',
                          headers=headers_faceit).json()
        maplist = player["segments"]
        for i in range(len(maplist)):
            if maplist[i]["label"] == map_name and maplist[i]["mode"] == "5v5":
                searched_map = maplist[i]
        nmap = parse_obj_as(schemas.Map, searched_map)
        nmap.img_regular = f'{maps[map_name]}'
        return nmap
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')

@router.get("/last_20_games_stats/{telegram_id}")
async def last_20_games_stats(telegram_id, db: Session = Depends(get_db)):
    teleid = db.query(models.Post).filter(models.Post.telegram_id == telegram_id).first()
    if teleid:
        players = parse_obj_as(schemas.Player, requests.get(f'https://open.faceit.com/data/v4/players?nickname={teleid.faceit_nickname}',
                                                headers=headers_faceit).json())
        player = requests.get(
            f"https://open.faceit.com/data/v4/players/{players.player_id}/history?game=csgo&offset=0&limit=20",
            headers=headers_faceit)
        match_time = {}
        responce = player.json()
        matches = responce["items"]
        for i in range(len(matches)):
            match_time[datetime.utcfromtimestamp(matches[i]["finished_at"]).strftime('%Y-%m-%d %H:%M:%S')] = matches[i]["match_id"]
        return match_time
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')
    
@router.get("/match_statistic/{telegram_id}/{match_id}")
async def match_statistic(telegram_id, match_id, db: Session = Depends(get_db)):
    teleid = db.query(models.Post).filter(models.Post.telegram_id == telegram_id).first()
    if teleid:
        stats = requests.get(f"https://open.faceit.com/data/v4/matches/{match_id}/stats", headers=headers_faceit).json()
        rounds = parse_obj_as(schemas.RoundStats, stats["rounds"][0]["round_stats"])
        for i in range(len(stats["rounds"][0]["teams"])):
            for j in range(len(stats["rounds"][0]["teams"][i]["players"])):
                if stats["rounds"][0]["teams"][i]["players"][j]["nickname"] == teleid.faceit_nickname:
                    player_stats = parse_obj_as(schemas.MapPlayerStats, stats["rounds"][0]["teams"][i]["players"][j]["player_stats"])
        player_stats.score = rounds.Score
        player_stats.mapname = rounds.Map
        player_stats.map_url = maps[f'{player_stats.mapname}']
        return player_stats
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')
    
@router.get("/global_position/{telegram_id}")
async def player_position(telegram_id, db: Session = Depends(get_db)):
    teleid = db.query(models.Post).filter(models.Post.telegram_id == telegram_id).first()
    if teleid:
        players = parse_obj_as(schemas.Player, requests.get(f'https://open.faceit.com/data/v4/players?nickname={teleid.faceit_nickname}',
                                                headers=headers_faceit).json())
        table = requests.get(f'https://open.faceit.com/data/v4/rankings/games/csgo/regions/{players.games.csgo.region}/players/{players.player_id}?limit=1', headers=headers_faceit).json()
        return table["position"], players.games.csgo.region
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')


@router.get("/country_position/{telegram_id}")
async def player_country_position(telegram_id, db: Session = Depends(get_db)):
    teleid = db.query(models.Post).filter(models.Post.telegram_id == telegram_id).first()
    if teleid:
        players = parse_obj_as(schemas.Player, requests.get(f'https://open.faceit.com/data/v4/players?nickname={teleid.faceit_nickname}',
                                                headers=headers_faceit).json())
        table = requests.get(f'https://open.faceit.com/data/v4/rankings/games/csgo/regions/{players.games.csgo.region}/players/{players.player_id}?country={players.country}&limit=1', headers=headers_faceit).json()
        return table["position"], players.country
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not registered')