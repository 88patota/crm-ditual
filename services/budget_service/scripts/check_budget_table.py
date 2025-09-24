from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"  # Substitua com sua URL de conexão

Base = declarative_base()

async def check_budget_table():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        inspector = inspect(conn)
        columns = inspector.get_columns("budgets")
        print("Colunas da tabela 'budgets':")
        for column in columns:
            print(f"- {column['name']} ({column['type']})")

if __name__ == "__main__":
    import asyncio
    asyncio.run(check_budget_table())
