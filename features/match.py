from .rating import calculate_new_rating
from fastapi import APIRouter, Depends
from modules.test_sqlalchemy import get_db, Team  
from modules.schemas import Result as ResultPydantic
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/match/{match_id}")
async def record_match(match_id: int, result: ResultPydantic, db: Session = Depends(get_db)):
    # отримуємо команди за їхніми id
    team_1 = db.query(Team).filter(Team.id == result.team_1_id).first()
    team_2 = db.query(Team).filter(Team.id == result.team_2_id).first()

    if not team_1 or not team_2:
        return {"error": "One or both teams not found"}

    # розрахунок нових рейтингів
    new_rating_team_1, new_rating_team_2 = calculate_new_rating(team_1.rating, team_2.rating)

    # оновлення рейтингів
    team_1.rating = new_rating_team_1
    team_2.rating = new_rating_team_2
    db.commit()

    return {"message": f"Match {match_id} recorded"}