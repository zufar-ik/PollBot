from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO main_user (name, username, id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def get_all_course(self):
        sql = 'SELECT * FROM main_poll_type'
        return await self.execute(sql, fetch=True)

    async def get_course(self, **kwargs):
        sql = "SELECT * FROM main_poll_type WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_users(self):
        sql = "SELECT * FROM main_user"
        return await self.execute(sql, fetch=True)

    async def select_all_group(self):
        sql = "SELECT * FROM main_group"
        return await self.execute(sql, fetch=True)

    async def all_tops(self, **kwargs):
        sql = 'SELECT * FROM main_poll_class WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def all_quest(self, **kwargs):
        sql = "SELECT * FROM main_poll WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def where_questions(self, **kwargs):
        sql = "SELECT * FROM main_poll WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def where_answer(self, **kwargs):
        sql = "SELECT * FROM main_poll_answer WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def user_answer_info(self, tg_id, name, poll_id, true_option, answer, point, chat_id):
        sql = "INSERT INTO main_user_answer (tg_id,name,poll_id,true_option,answer,point,chat_id) VALUES($1,$2,$3,$4,$5,$6,$7) returning *"
        return await self.execute(sql, tg_id, name, poll_id, true_option, answer, point, chat_id, fetchrow=True)

    async def views_user_answer(self, **kwargs):
        sql = "SELECT * FROM main_user_answer WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def drop_users_answer(self, **kwargs):
        sql = "DELETE FROM main_user_answer WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def add_group(self, chat_id, name):
        sql = 'INSERT INTO main_group (group_id,name) VALUES ($1, $2) returning *'
        return await self.execute(sql, chat_id, name, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM main_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM main_user"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE main_user SET username=$1 WHERE id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM main_user WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE main_user", execute=True)
