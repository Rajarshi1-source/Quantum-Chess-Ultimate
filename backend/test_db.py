import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

load_dotenv()  # reads from .env file in project root

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:YOUR_PASSWORD_HERE@localhost:5432/quantum_chess",
)

async def test():
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print("Database connected successfully!")

asyncio.run(test())
