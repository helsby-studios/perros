from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
import db

# to interact with the database, import * from this file (includes the session object and any other functions you need)
# example usage:
# --------------------
# example 1:
# from db_driver import session
# async def some_function():
#     result = await session.execute(select(db.cogdata).filter_by(cogid=1))
#     return result.scalars().first()

# example 2:
# from db_driver import add_cogdata
# async def some_function():
#     new_cogdata = await add_cogdata(1, "test", "test", "test", "test", "test", "test")
#     return new_cogdata

# --------------------
Session = sessionmaker(bind=db.engine, class_=AsyncSession)
session = Session()


# some functions to interact with the database (cog data)
async def add_cogdata(cogid, cog, name, value, data1, data2, data3):
    new_cogdata = db.cogdata(cogid, cog, name, value, data1, data2, data3)
    session.add(new_cogdata)
    await session.commit()
    return new_cogdata


async def get_cogdata(cogid):
    result = await session.execute(select(db.cogdata).filter_by(cogid=cogid))
    return result.scalars().first()


async def get_cogdata_by_name(name):
    result = await session.execute(select(db.cogdata).filter_by(name=name))
    return result.scalars().first()


async def get_cogdata_by_cog(cog):
    result = await session.execute(select(db.cogdata).filter_by(cog=cog))
    return result.scalars().all()


async def update_cogdata(id, cogid, cog, name, value, data1, data2, data3):
    result = await session.execute(select(db.cogdata).filter_by(id=id))
    cogdata = result.scalars().first()
    cogdata.cogid = cogid
    cogdata.cog = cog
    cogdata.name = name
    cogdata.value = value
    cogdata.data1 = data1
    cogdata.data2 = data2
    cogdata.data3 = data3
    await session.commit()
    return cogdata


async def delete_cogdata(id):
    cogdata = await session.query(db.cogdata).filter_by(id=id).first()
    session.delete(cogdata)
    await session.commit()
    return cogdata


async def add_config(name, value):
    new_config = db.config(name, value)
    session.add(new_config)
    await session.commit()
    return new_config


# some functions to interact with the database (config)
async def get_config(name):
    result = await session.execute(select(db.config).filter_by(name=name))
    return result.scalars().first()


async def get_config_by_value(value):
    result = await session.execute(select(db.config).filter_by(value=value))
    return result.scalars().first()


async def get_config_by_id(id):
    result = await session.execute(select(db.config).filter_by(id=id))
    return result.scalars().first()


async def get_all_config():
    result = await session.execute(select(db.config))
    return result.scalars().all()


async def update_config(id, name, value):
    result = await session.execute(select(db.config).filter_by(id=id))
    config = result.scalars().first()
    config.name = name
    config.value = value
    await session.commit()
    return config


async def delete_config(id):
    config = await session.query(db.config).filter_by(id=id).first()
    session.delete(config)
    await session.commit()
    return config


# game related stuff
async def add_game(guildid, difficulty, day, map):
    new_game = db.game(guildid, difficulty, day, map)
    session.add(new_game)
    await session.commit()
    return new_game


async def get_game(guildid):
    result = await session.execute(select(db.game).filter_by(guildid=guildid))
    return result.scalars().first()


async def delete_game(guildid):
    game = await session.execute(select(db.game).filter_by(guildid=guildid)).scalars().first()
    session.delete(game)
    await session.commit()
    return game
