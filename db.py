import asyncio

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine('sqlite+aiosqlite:///db.sqlite' + '?check_same_thread=False', echo=True)

base = declarative_base()

# base config DB for the bot
class config(base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    value = Column(String)

    def __init__(self, name, value):
        self.name = name
        self.value = value

# expand as needed...

# data storage for cogs
class cogdata(base):
    __tablename__ = 'cogdata'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cogid = Column(Integer)
    cog = Column(String)
    name = Column(String)
    value = Column(String)
    data1 = Column(String)
    data2 = Column(String)
    data3 = Column(String)

    def __init__(self, cogid, cog, name, value, data1, data2, data3):
        self.cogid = cogid
        self.cog = cog
        self.name = name
        self.value = value
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3

# game stuff
class game(base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True, autoincrement=True)
    guildid = Column(Integer)
    difficulty = Column(String)
    day = Column(Integer)
    map = Column(String)

    def __init__(self, guildid, difficulty, day, map):
        self.guildid = guildid
        self.difficulty = difficulty
        self.day = day
        self.map = map
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)

asyncio.run(init_models())