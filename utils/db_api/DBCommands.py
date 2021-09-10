from aiogram import types

from .database import db
from .models import User


class DBCommands:

    async def get_user(self, user_id=None, user_name=None) -> User:
        if user_id is not None:
            user = await User.query.where(User.user_id == user_id).gino.first()
            return user
        elif user_id is None and user_name is not None:
            user = await User.query.where(User.username == user_name).gino.first()
            return user

    async def add_new_user(self, referral=None):
        user = types.User.get_current()

        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name

        if referral:
            new_user.referral = int(referral)
        await new_user.create()
        return new_user

    async def update_user_data(self, **kwargs):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(**kwargs).apply()
        return user_id

    async def get_user_data(self) -> User:
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        return user

    async def count_users(self) -> int:
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def get_all_users(self) -> list[User]:
        return await User.query.gino.all()

