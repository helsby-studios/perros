from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
import db

# to interact with the database, import * from this file (includes the session object and any other functions you need)
# example usage:
# --------------------
# example 1:
#from db_driver import *
#import asyncio
#
#async def main():
#    await add_config('test', 'test')
#
#if __name__ == '__main__':
#    asyncio.run(main())
# example 2:
#from db_driver import *
#import asyncio
#
#async def main():
#    config = await session.query(db.config).filter_by(name="test").first()
#    print(config.value)
#
#if __name__ == '__main__':
#    asyncio.run(main())
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
    return await session.query(db.cogdata).filter_by(cogid=cogid).first()

async def get_cogdata_by_name(name):
    return await session.query(db.cogdata).filter_by(name=name).first()

async def get_cogdata_by_cog(cog):
    return await session.query(db.cogdata).filter_by(cog=cog).first()

async def update_cogdata(id, cogid, cog, name, value, data1, data2, data3):
    cogdata = await session.query(db.cogdata).filter_by(id=id).first()
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
    return await session.query(db.config).filter_by(name=name).first()

async def get_config_by_value(value):
    return await session.query(db.config).filter_by(value=value).first()

async def get_config_by_id(id):
    return await session.query(db.config).filter_by(id=id).first()

async def get_all_config():
    return await session.query(db.config).all()

async def update_config(id, name, value):
    config = await session.query(db.config).filter_by(id=id).first()
    config.name = name
    config.value = value
    await session.commit()
    return config

async def delete_config(id):
    config = await session.query(db.config).filter_by(id=id).first()
    session.delete(config)
    await session.commit()
    return config