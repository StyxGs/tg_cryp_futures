# Работа с базой данных
from sqlalchemy import Result, Select, select
from sqlalchemy.dialects.postgresql import Insert, insert
from sqlalchemy.orm import selectinload

from database.database_connection import async_session_maker
from model.models import CrypFuture, TgUser


class BotDB:
    """Класс для работы с базой данных"""

    @staticmethod
    async def check_user_in_db(user_id: int, username: str | None) -> None:
        """Проверяем есть ли пользователь в базе, если нет то добавляем"""
        data: dict = {'tg_user_id': user_id, 'tg_username': username}
        async with async_session_maker() as session:
            stmt: Insert = insert(TgUser).values(data).on_conflict_do_nothing(
                index_elements=['tg_user_id'])
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_future_in_list(tg_user_id: int, future: str) -> None:
        """Добавляет фьючерс в список отслеживаемых пользователем"""
        data: dict = {'title': future}
        async with async_session_maker() as session:
            query_future = await session.scalars(insert(CrypFuture).values(data).on_conflict_do_nothing(
                index_elements=['title']).returning(CrypFuture))
            query_user = await session.scalars(select(TgUser).where(TgUser.tg_user_id == tg_user_id).options(
                selectinload(TgUser.cryp_future)))
            user = query_user.first()
            fch = query_future.first()
            if fch:
                user.cryp_future.append(fch)
                await session.commit()

    @staticmethod
    async def show_my_list_futures(tg_user_id: int) -> list:
        """Отдаёт список фьючерсов отслеживаемых пользователем"""
        async with async_session_maker() as session:
            query: Select = select(TgUser).where(TgUser.tg_user_id == tg_user_id).options(
                selectinload(TgUser.cryp_future))
            result: Result = await session.scalars(query)
            return [crfch.title for crfch in result.first().cryp_future]

    @staticmethod
    async def delete_future_in_my_list(tg_user_id: int, future: str) -> None:
        """Удаляет фьючерс из списка отслеживаемых"""
        async with async_session_maker() as session:
            query_future = await session.scalars(select(CrypFuture).where(CrypFuture.title == future))
            query_user = await session.scalars(select(TgUser).where(TgUser.tg_user_id == tg_user_id).options(
                selectinload(TgUser.cryp_future)))
            user = query_user.first()
            fch = query_future.first()
            user.cryp_future.remove(fch)
            await session.commit()
