from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from auth import create_access_token, verify_access_token, get_current_user, UserLogin
from test import User as UserPydantic, Result as ResultPydantic, Team as TeamPydantic, Tournament as TournamentPydantic
from test_sqlalchemy import get_db, Session, User, Result, Tournament, Team, \
    result_team_association, result_user_association, result_tournament_association, \
    user_team_association

from database import engine
from test_sqlalchemy import Base

Base.metadata.create_all(bind=engine)
print("Таблиці створені автоматично")

router = APIRouter()

@router.post("/token")
async def login_for_access_token(user: UserLogin): 
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

app = FastAPI()

@app.post('/user', summary="Registration of users")
async def user_add(user: UserPydantic, db: Session = Depends(get_db)):
    user_DB = db.query(User).filter(User.email == user.email).first()
    if user_DB:
        raise HTTPException(status_code=400, detail="User with this email already exists!")
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'user': new_user, 'message': "User has been added to the DB!"}

@app.post('/result')
async def add_result(result: ResultPydantic, db: Session = Depends(get_db)):
    name_team = result.team.name
    name_tournament = result.tournament.name
    email_user_mvp = result.mvp.email

    mvp_from_DB = db.query(User).filter(User.email == email_user_mvp).first()
    tournament_DB = db.query(Tournament).filter(Tournament.name == name_tournament).order_by(desc(Tournament.id)).first()
    team_DB = db.query(Team).filter(Team.name == name_team).first()

    if not mvp_from_DB or not tournament_DB or not team_DB:
        raise HTTPException(status_code=404, detail="Something happened! User or Team or Tournament do not exist!")

    new_result = Result(score=result.score)
    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    db.execute(result_user_association.insert().values({'result_id': new_result.id, 'user_id': mvp_from_DB.id}))
    db.execute(result_tournament_association.insert().values({'result_id': new_result.id, 'tournament_id': tournament_DB.id}))
    db.execute(result_team_association.insert().values({'result_id': new_result.id, 'team_id': team_DB.id}))
    db.commit()

    return {'result': result, 'message': "Result has been added to the DB!"}

@app.post('/team')
async def add_team(team: TeamPydantic, db: Session = Depends(get_db)):
    team_DB = db.query(Team).filter(Team.name == team.name).first()
    if team_DB:
        raise HTTPException(status_code=400, detail="Team with this name already exists!")

    new_team = Team(name=team.name, description=team.description)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    for email in team.users:
        user = db.query(User).filter(User.email == email).first()
        if user:
            db.execute(user_team_association.insert().values({"user_id": user.id, "team_id": new_team.id}))

    db.commit()
    return {'Team': team, 'message': "Team has been added to the DB!"}

@app.post('/tournament')
async def add_tournament(tournament: TournamentPydantic, db: Session = Depends(get_db)):
    tournament_DB = db.query(Tournament).filter(Tournament.name == tournament.name).first()
    if tournament_DB:
        raise HTTPException(status_code=400, detail="Tournament with this name already exists!")

    if tournament.end_date <= tournament.start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date.")

    new_tournament = Tournament(
        name=tournament.name,
        description=tournament.description,
        reward=tournament.reward,
        rules=tournament.rules,
        start_date=tournament.start_date,
        end_date=tournament.end_date
    )
    db.add(new_tournament)
    db.commit()
    db.refresh(new_tournament)

    return {'Tournament': tournament, 'message': "Tournament has been added to the DB!"}

app.include_router(router)