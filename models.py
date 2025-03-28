from fastapi import Query, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Dict
import datetime
import re


class UserModel(BaseModel):
    username: str = Query(..., min_length=5, max_length=20)
    email: EmailStr
    password: str
    phone: str
    age: int = Query(..., gte=14)

    @field_validator('phone')
    @classmethod
    def verify_phone(cls, phone: str) -> str:
        if not re.match(r'^\+?[1-9]\d{1,14}$', phone):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid phone number')
        return phone

    @field_validator('password')
    @classmethod
    def validate_password(cls, password):
        if not re.search(r'[^a-zA-Z0-9]', password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password')
        return password


class UserModeljson(BaseModel):
    userresponse: List[UserModel]


class TeamModel(BaseModel):
    name: str = Query(..., max_length=20)
    description: str = Query(..., max_length=500)
    userlist: List[str]


class TeamModeljson(BaseModel):
    teamresponse: List[TeamModel]


class TournamentModel(BaseModel):
    name: str = Query(..., max_length=20)
    description: str = Query(..., max_length=500)
    reward: str = Query(..., max_length=100)
    rules: Dict[str, str]
    start_date: datetime.datetime
    end_date: datetime.datetime
    close_reg: datetime.datetime
    teamlist: List[str]

    @field_validator('start_date', 'end_date', 'close_reg')
    @classmethod
    def validate_datetime(cls, value):
        if value.date() < datetime.datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The date {value} cannot be in the past')
        return value


class TournamentModeljson(BaseModel):
    tournamentmodel: List[TournamentModel]


class ResultModel(BaseModel):
    tournament: str
    mvp: str = Query(None, max_length=20)
    team: str
    score: str


class ResultModeljson(BaseModel):
    resultmodel: List[ResultModel]
