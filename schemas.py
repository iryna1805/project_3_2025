from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class TeamCreate(BaseModel):
    name: str

class TournamentCreate(BaseModel):
    name: str
    date: Optional[datetime] = None

class ResultCreate(BaseModel):
    score: int
    team_id: int
    tournament_id: int

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Team(BaseModel):
    id: int
    name: str
    user_id: int

    class Config:
        orm_mode = True

class Tournament(BaseModel):
    id: int
    name: str
    date: datetime

    class Config:
        orm_mode = True

class Result(BaseModel):
    id: int
    score: int
    team_id: int
    tournament_id: int

    class Config:
        orm_mode = True
