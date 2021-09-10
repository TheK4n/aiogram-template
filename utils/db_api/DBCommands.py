from aiogram import types

from .database import db
from .models import User, Group, Sender


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

    async def add_new_group(self, user_id: int, group_name: str, group_id: str):
        new_group = Group()
        new_group.group_name = group_name
        new_group.group_id = group_id
        new_group.user_id = user_id
        await new_group.create()
        return new_group

    async def set_group_sender(self, group_id, user_id, message, image, interval):

        new_sender = Sender()
        new_sender.message = message
        new_sender.group_id = group_id
        new_sender.image = image
        new_sender.interval = interval
        new_sender.user_id = user_id
        await new_sender.create()
        return new_sender

    async def get_sender(self, id_global: int):
        return await Sender.query.where(Sender.id == id_global).gino.first()

    async def del_sender(self, id_global: int):
        await (await Sender.query.where(Sender.id == id_global).gino.first()).delete()

    async def get_senders_by_interval(self, interval: int):
        return await Sender.query.where(Sender.interval == interval).gino.all()

    async def get_user_groups(self):
        user = types.User.get_current()
        return await Group.query.where(Group.user_id == user.id).gino.all()

    async def get_user_senders_by_group(self, group_id):
        user = types.User.get_current()
        return await Sender.query.where(Sender.user_id == user.id and Sender.group_id == group_id).gino.all()
