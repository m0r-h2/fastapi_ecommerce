import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import async_session_maker  # твой async sessionmaker
from app.db.models import Category


async def seed_categories():
    async with async_session_maker() as session:  # type: AsyncSession

        # --- создаём корневые категории ---
        electronics = Category(name="Electronics")
        home_appliances = Category(name="Home Appliances")
        clothing = Category(name="Clothing")
        books = Category(name="Books")
        sports = Category(name="Sports")

        session.add_all([electronics, home_appliances, clothing, books, sports])

        await session.flush()  # получаем id без commit

        # --- подкатегории ---
        session.add_all(
            [
                Category(name="Smartphones", parent_id=electronics.id),
                Category(name="Laptops", parent_id=electronics.id),
                Category(name="Tablets", parent_id=electronics.id),
                Category(name="Refrigerators", parent_id=home_appliances.id),
                Category(name="Washing Machines", parent_id=home_appliances.id),
                Category(name="Microwaves", parent_id=home_appliances.id),
                Category(name="Men's Clothing", parent_id=clothing.id),
                Category(name="Women's Clothing", parent_id=clothing.id),
                Category(name="Kids' Clothing", parent_id=clothing.id),
                Category(name="Fiction", parent_id=books.id),
                Category(name="Non-Fiction", parent_id=books.id),
                Category(name="Children's Books", parent_id=books.id),
                Category(name="Fitness Equipment", parent_id=sports.id),
                Category(name="Outdoor Gear", parent_id=sports.id),
                Category(name="Cycling", parent_id=sports.id),
            ]
        )

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_categories())
