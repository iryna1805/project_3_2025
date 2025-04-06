from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class Team(BaseModel):
    name: str
    description: str
    users: List[EmailStr]


class Tournament(BaseModel):
    name: str
    description: str
    reward: str
    rules: str
    start_date: datetime
    end_date: datetime


class Result(BaseModel):
    score: int
    mvp: User
    team: Team
    tournament: Tournament
