from pydantic import BaseModel, Field
from typing import Optional,  List
from typing import Optional


class CSGO(BaseModel):
    region: str
    game_player_id: str
    skill_level: int
    faceit_elo: int
    game_player_name: str


class Games(BaseModel):
    csgo: Optional[CSGO] = None


class Language(BaseModel):
    language: str


class Player(BaseModel):
    nickname: str
    player_id: str
    nickname: str
    avatar: str
    country: str
    games: Optional[Games] = None
    steam_id_64: str
    steam_nickname: str
    settings: Language
    memberships: list
    friends_ids: List[str]
    search_count: Optional[int] = None


class Lifetime(BaseModel):
    winrate: str = Field(alias='Win Rate %')
    recent_results: list = Field(alias='Recent Results')
    total_headshots: str = Field(alias='Total Headshots %')
    average_kd_ratio: str = Field(alias='Average K/D Ratio')
    longest_win_streak: str = Field(alias='Longest Win Streak')
    wins: str = Field(alias='Wins')
    average_headshots: str = Field(alias='Average Headshots %')
    matches: str = Field(alias='Matches')


class Stats(BaseModel):
    lifetime: Lifetime


class Map_stats(BaseModel):
    average_penta_kills: str = Field(alias='Average Penta Kills')
    Wins: str
    average_triple_kills: str = Field(alias='Average Triple Kills')
    Matches: str
    average_kd_ratio: str = Field(alias='Average K/D Ratio')
    Headshots: str
    kr_ratio: str = Field(alias='K/R Ratio')
    winrate: str = Field(alias='Win Rate %')
    Kills: str
    total_headshots: str = Field(alias='Total Headshots %')
    average_headsots: str = Field(alias='Average Headshots %')
    MVPs: str
    quadro_kills: str = Field(alias='Quadro Kills')
    penta_kills: str = Field(alias='Penta Kills')
    average_assists: str = Field(alias='Average Assists')
    average_kills: str = Field(alias='Average Kills')
    triple_kills: str = Field(alias='Triple Kills')
    Deaths: str
    average_mvps: str = Field(alias='Average MVPs')
    average_kr_ratio: str = Field(alias='Average K/R Ratio')
    Assists: str
    headshots_per_match: str = Field(alias='Headshots per Match')
    Rounds: str
    average_qadro_kills: str = Field(alias='Average Quadro Kills')
    average_deaths: str = Field(alias='Average Deaths')\

class Map(BaseModel):
    img_regular: str
    stats: Map_stats



class RoundStats(BaseModel):
    Score: str
    Map: str


class MapPlayerStats(BaseModel):
    Headshots: str
    Result: str
    Quadro_kills: str = Field(alias='Quadro Kills')
    MVPs: str
    kd_ratio: str = Field(alias='K/D Ratio')
    Deaths: str
    headshots_percentage: str = Field(alias='Headshots %')
    penta_kills: str = Field(alias='Penta Kills')
    kr_ratio: str = Field(alias='K/R Ratio')
    triple_kills: str = Field(alias='Triple Kills')
    Kills: str
    Headshots: str
    Assists: str
    score: Optional[str] = None
    mapname: Optional[str] = None
    map_url: Optional[str] = None


class DisplayValue(BaseModel):
    displayValue: str
    

class Model(BaseModel):
    timePlayed: DisplayValue
    kills: DisplayValue
    deaths: DisplayValue
    kd: DisplayValue
    damage: DisplayValue
    headshots: DisplayValue
    shotsFired: DisplayValue
    shotsHit: DisplayValue
    shotsAccuracy: DisplayValue
    bombsPlanted: DisplayValue
    bombsDefused: DisplayValue
    moneyEarned: DisplayValue
    hostagesRescued: DisplayValue
    mvp: DisplayValue
    wins: DisplayValue
    matchesPlayed: DisplayValue
    losses: DisplayValue
    roundsPlayed: DisplayValue
    roundsWon: DisplayValue
    headshotPct: DisplayValue



class Metadata(BaseModel):
    name: str
    imageUrl: str
    category: str

class Stats_Weapon(BaseModel):
    kills: DisplayValue
    shotsFired: DisplayValue
    shotsHit: DisplayValue
    shotsAccuracy: DisplayValue


class Model_Weapon(BaseModel):
    metadata: Metadata
    expiryDate: str
    stats: Stats_Weapon

class Account(BaseModel):
    faceit_nickname: str
    telegram_id: str
    search_count: Optional[int] = 0