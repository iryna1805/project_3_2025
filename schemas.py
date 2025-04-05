from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional
import datetime


class UserModel(BaseModel):
    username: str = Field(..., min_length=5, max_length=20)
    email: EmailStr
    password: str
    phone: str
    age: int = Field(..., ge=14)


class TeamModel(BaseModel):
    name: str = Field(..., max_length=20)
    description: str = Field(..., max_length=500)
    userlist: List[str]


class TournamentModel(BaseModel):
    name: str = Field(..., max_length=20)
    description: str = Field(..., max_length=500)
    reward: str = Field(..., max_length=100)
    rules: Dict[str, str]
    start_date: datetime.datetime
    end_date: datetime.datetime
    close_reg: datetime.datetime
    teamlist: List[str]


class ResultModel(BaseModel):
    tournament: str
    mvp: Optional[str] = Field(None, max_length=20)
    team: str
    score: str
