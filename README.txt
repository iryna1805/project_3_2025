to start the programm:
pip install uvicorn fastapi aiomysql pydantic[all] typing datetime re
uvicorn main:app --reload

# FastAPI Tournament Manager

Це REST API для керування користувачами, командами, турнірами та результатами з використанням FastAPI + SQLAlchemy.

## Технології:

- **FastAPI** — основний фреймворк
- **SQLAlchemy** — ORM для бази даних
- **Pydantic** — валідація даних
- **SQLite** — база даних (можна легко замінити на PostgreSQL)

##        Встановлення

```bash
git clone <url>
cd <назва-папки>
python -m venv .venv
source .venv/bin/activate # або .venv\Scripts\activate (Windows)
pip install -r requirements.txt

task:
task.pdf