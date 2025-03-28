import aiomysql
from fastapi import Depends
from typing import AsyncGenerator


class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                host='localhost',
                port=3306,
                user='root',
                password='password',
                db='db',
                autocommit=True,
                minsize=5,
                maxsize=10,
            )

    async def disconnect(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def execute_query(self, query: str, params=None):
        await self.connect()
        async with self.pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params)
                if query.strip().lower().startswith('select'):
                    return await cursor.fetchall()
                elif query.strip().lower().startswith(('insert', 'update', 'delete')):
                    return {'message': 'Query executed successfully'}

    @staticmethod
    async def create_database():
        conn = await aiomysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='password',
            autocommit=True
        )
        async with conn.cursor() as cursor:
            await cursor.execute('CREATE DATABASE IF NOT EXISTS db;')
        conn.close()
        await conn.wait_closed()

    async def create_tables(self):
        await self.execute_query("""
        CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(20) UNIQUE NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        phone VARCHAR(50),
        age INT NOT NULL
        );
        """)

        await self.execute_query("""
        CREATE TABLE IF NOT EXISTS teams (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(20) UNIQUE NOT NULL,
        description TEXT
        userlist TEXT
        );
        """)

        await self.execute_query("""
        CREATE TABLE IF NOT EXISTS tournaments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(20) UNIQUE NOT NULL,
        description TEXT,
        reward VARCHAR(100),
        rules TEXT,
        start_date DATETIME,
        end_date DATETIME,
        close_reg DATETIME,
        teamlist TEXT
        );
        """)

        await self.execute_query("""
        CREATE TABLE IF NOT EXISTS results(
        id INT AUTO_INCREMENT PRIMARY KEY,
        tournament TEXT,
        mvp VARCHAR(20),
        team TEXT,
        score TEXT
        );
        """)

    async def get_connection(self) -> AsyncGenerator[aiomysql.Connection, None]:
        await self.connect()
        async with self.pool.acquire() as conn:
            yield conn


db_manager = DatabaseManager()


async def get_db(conn=Depends(db_manager.get_connection)):
    return conn
