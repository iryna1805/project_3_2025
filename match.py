from .rating import calculate_new_rating

@router.post("/match/{match_id}")
async def record_match(match_id: int, result: ResultModel):
    # отримуємо команди та їх рейтинги
    team_1 = db.query(Team).filter(Team.id == result.team_1_id).first()
    team_2 = db.query(Team).filter(Team.id == result.team_2_id).first()

    # розрахунок нових рейтингів
    new_rating_team_1, new_rating_team_2 = calculate_new_rating(team_1.rating, team_2.rating)

    # оновлення рейтингу в базі даних
    team_1.rating = new_rating_team_1
    team_2.rating = new_rating_team_2
    db.commit()
