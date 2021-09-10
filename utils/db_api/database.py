from gino import Gino

from data.config import PG_HOST, PG_USER, PG_PASS

db = Gino()


async def create_db():
    await db.set_bind(f'postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}/gino1')

    # Create tables
    # await db.gino.drop_all()
    # await db.gino.create_all()
