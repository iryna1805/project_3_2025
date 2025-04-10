from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from modules.auth import create_access_token, verify_access_token, get_current_user, UserLogin
from modules.schemas import User as UserPydantic, Result as ResultPydantic, Team as TeamPydantic, Tournament as TournamentPydantic
from modules.test_sqlalchemy import get_db, Session, User, Result, Tournament, Team, \
    result_team_association, result_user_association, result_tournament_association, \
    user_team_association
from modules.database import engine
from modules.test_sqlalchemy import Base
from features.match import router as match_router, record_match
from features.notifications import send_email, start_websocket_server
import asyncio

Base.metadata.create_all(bind=engine)
print("Таблиці створені автоматично")

app = FastAPI()
router = APIRouter()

@app.on_event("startup")
async def startup():
    # Запускаємо сервер websockets паралельно з FastAPI
    asyncio.create_task(start_websocket_server())


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(match_router)

@router.post("/token")
async def login_for_access_token(user: UserLogin):
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# ------------------- USERS ------------------
@app.post('/user')
async def user_add(user: UserPydantic, db: Session = Depends(get_db)):
    user_DB = db.query(User).filter(User.email == user.email).first()
    if user_DB:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user": new_user}

@app.put('/user/{email}')
async def update_user(email: str, updated: UserPydantic, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = updated.username
    user.password = updated.password
    db.commit()
    return {"message": "User updated"}

@app.delete('/user/{email}')
async def delete_user(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

# ------------------- TEAMS ------------------
@app.post('/team')
async def add_team(team: TeamPydantic, db: Session = Depends(get_db)):
    team_DB = db.query(Team).filter(Team.name == team.name).first()
    if team_DB:
        raise HTTPException(status_code=400, detail="Team exists")
    new_team = Team(name=team.name, description=team.description)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    for email in team.users:
        user = db.query(User).filter(User.email == email).first()
        if user:
            db.execute(user_team_association.insert().values({"user_id": user.id, "team_id": new_team.id}))
    db.commit()
    return {"team": team}

@app.put('/team/{name}')
async def update_team(name: str, updated: TeamPydantic, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.name == name).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team.name = updated.name
    team.description = updated.description
    db.commit()
    return {"message": "Team updated"}

@app.delete('/team/{name}')
async def delete_team(name: str, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.name == name).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(team)
    db.commit()
    return {"message": "Team deleted"}

# ------------------- TOURNAMENTS ------------------
@app.post('/tournament')
async def add_tournament(tournament: TournamentPydantic, db: Session = Depends(get_db)):
    if tournament.end_date <= tournament.start_date:
        raise HTTPException(status_code=400, detail="Invalid dates")
    new_tournament = Tournament(**tournament.dict())
    db.add(new_tournament)
    db.commit()
    db.refresh(new_tournament)
    return {"tournament": tournament}

@app.put('/tournament/{name}')
async def update_tournament(name: str, updated: TournamentPydantic, db: Session = Depends(get_db)):
    tournament = db.query(Tournament).filter(Tournament.name == name).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    for field, value in updated.dict().items():
        setattr(tournament, field, value)
    db.commit()
    return {"message": "Tournament updated"}

@app.delete('/tournament/{name}')
async def delete_tournament(name: str, db: Session = Depends(get_db)):
    tournament = db.query(Tournament).filter(Tournament.name == name).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    db.delete(tournament)
    db.commit()
    return {"message": "Tournament deleted"}

# ------------------- RESULTS ------------------
@app.post('/result')
async def add_result(result: ResultPydantic, db: Session = Depends(get_db)):
    mvp = db.query(User).filter(User.email == result.mvp.email).first()
    team = db.query(Team).filter(Team.name == result.team.name).first()
    tournament = db.query(Tournament).filter(Tournament.name == result.tournament.name).order_by(desc(Tournament.id)).first()
    if not mvp or not team or not tournament:
        raise HTTPException(status_code=404, detail="Invalid MVP/Team/Tournament")
    new_result = Result(score=result.score)
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    db.execute(result_user_association.insert().values({'result_id': new_result.id, 'user_id': mvp.id}))
    db.execute(result_team_association.insert().values({'result_id': new_result.id, 'team_id': team.id}))
    db.execute(result_tournament_association.insert().values({'result_id': new_result.id, 'tournament_id': tournament.id}))
    db.commit()
    return {'result': result}

@app.delete('/result/{result_id}')
async def delete_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    db.delete(result)
    db.commit()
    return {"message": "Result deleted"}

# ------------------- MATCH ROUTE ------------------
@app.post('/match/{match_id}')
async def match_result(match_id: int, result: ResultPydantic, db: Session = Depends(get_db)):
    return await record_match(match_id, result)

# ------------------- NOTIFICATION TEST ------------------
@app.get("/notify/{email}")
async def test_notify(email: str):
    subject = "Нагадування про матч"
    body = "Привіт! Ваш матч скоро почнеться."
    await send_email(subject, body, email)
    return {"message": f"Email sent to {email}"}

app.include_router(router)
