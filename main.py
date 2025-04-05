from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, init_db

app = FastAPI()

# Initialize the database tables (called once when starting the app)
init_db()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations for Users
@app.post("/users/", response_model=schemas.UserModel)
def create_user(user: schemas.UserModel, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[schemas.UserModel])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/users/{user_id}", response_model=schemas.UserModel)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# CRUD operations for Teams
@app.post("/teams/", response_model=schemas.TeamModel)
def create_team(team: schemas.TeamModel, db: Session = Depends(get_db)):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@app.get("/teams/", response_model=List[schemas.TeamModel])
def get_teams(db: Session = Depends(get_db)):
    return db.query(models.Team).all()

# CRUD operations for Tournaments
@app.post("/tournaments/", response_model=schemas.TournamentModel)
def create_tournament(tournament: schemas.TournamentModel, db: Session = Depends(get_db)):
    db_tournament = models.Tournament(**tournament.dict())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

@app.get("/tournaments/", response_model=List[schemas.TournamentModel])
def get_tournaments(db: Session = Depends(get_db)):
    return db.query(models.Tournament).all()

# CRUD operations for Results
@app.post("/results/", response_model=schemas.ResultModel)
def create_result(result: schemas.ResultModel, db: Session = Depends(get_db)):
    db_result = models.Result(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

@app.get("/results/", response_model=List[schemas.ResultModel])
def get_results(db: Session = Depends(get_db)):
    return db.query(models.Result).all()
