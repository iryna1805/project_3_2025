from fastapi import FastAPI, HTTPException, status
from database import db_manager
from models import UserModel, TeamModel, TournamentModel, ResultModel

app = FastAPI()

"""========== USERS =========="""


@app.post('/users')
async def create_user(user: UserModel):
    try:
        await db_manager.execute_query("""
        INSERT INTO users(username, email, password, phone, age)
        VALUES (%s, %s, %s, %s, %s)
        """, (user.username, user.email, user.password, user.phone, user.age))
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/users')
async def get_users():
    return await db_manager.execute_query("SELECT * FROM users")


@app.put('/users/{username}')
async def update_user(username: str, user: UserModel):
    try:
        await db_manager.execute_query("""
        UPDATE users SET email=%s, password=%s, phone=%s, age=%s WHERE username=%s
        """, (user.email, user.password, user.phone, user.age, username))
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete('/users/{username}')
async def delete_user(username: str):
    try:
        await db_manager.execute_query("DELETE FROM users WHERE username=%s", (username,))
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


"""========== TEAMS =========="""


@app.post('/teams')
async def create_team(team: TeamModel):
    try:
        await db_manager.execute_query("""
        INSERT INTO teams(name, description) VALUES (%s, %s)
        """, (team.name, team.description))
        return {"message": "Team created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get('/teams')
async def get_teams():
    return await db_manager.execute_query("SELECT * FROM teams")


@app.put('/teams/{team_name}')
async def update_team(team_name: str, team: TeamModel):
    try:
        await db_manager.execute_query("""
        UPDATE teams SET description=%s WHERE name=%s
        """, (team.description, team_name))
        return {"message": "Team updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete('/teams/{team_name}')
async def delete_team(team_name: str):
    try:
        await db_manager.execute_query("DELETE FROM teams WHERE name=%s", (team_name,))
        return {"message": "Team deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


"""========== TOURNAMENTS =========="""


@app.post('/tournaments')
async def create_tournament(tournament: TournamentModel):
    try:
        await db_manager.execute_query("""
        INSERT INTO tournaments(name, description, reward, rules, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (tournament.name, tournament.description, tournament.reward, tournament.rules,
              tournament.start_date, tournament.end_date))
        return {"message": "Tournament created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get('/tournaments')
async def get_tournaments():
    return await db_manager.execute_query("SELECT * FROM tournaments")


@app.put('/tournaments/{tournament_name}')
async def update_tournament(tournament_name: str, tournament: TournamentModel):
    try:
        await db_manager.execute_query("""
        UPDATE tournaments SET description=%s, reward=%s, rules=%s, start_date=%s, end_date=%s WHERE name=%s
        """, (tournament.description, tournament.reward, tournament.rules, tournament.start_date,
              tournament.end_date, tournament_name))
        return {"message": "Tournament updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete('/tournaments/{tournament_name}')
async def delete_tournament(tournament_name: str):
    try:
        await db_manager.execute_query("DELETE FROM tournaments WHERE name=%s", (tournament_name,))
        return {"message": "Tournament deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


"""========== RESULTS =========="""


@app.post('/results')
async def create_result(result: ResultModel):
    try:
        await db_manager.execute_query("""
        INSERT INTO results(tournament_id, mvp_id, team_id, score)
        VALUES (%s, %s, %s, %s)
        """, (result.tournament_id, result.mvp_id, result.team_id, result.score))
        return {"message": "Result created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get('/results')
async def get_results():
    return await db_manager.execute_query("SELECT * FROM results")


@app.put('/results/{result_id}')
async def update_result(result_id: int, result: ResultModel):
    try:
        await db_manager.execute_query("""
        UPDATE results SET tournament_id=%s, mvp_id=%s, team_id=%s, score=%s WHERE id=%s
        """, (result.tournament_id, result.mvp_id, result.team_id, result.score, result_id))
        return {"message": "Result updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete('/results/{result_id}')
async def delete_result(result_id: int):
    try:
        await db_manager.execute_query("DELETE FROM results WHERE id=%s", (result_id,))
        return {"message": "Result deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
