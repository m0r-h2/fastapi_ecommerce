from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Category as CategoryModel
from app.core.exceptions import (
    CategoryNotFoundError,
    ParentCategoryNotFoundError,
    CategorySelfParentError,
)


async def get_all_categories_db(db: AsyncSession):
    result = await db.execute(
        select(CategoryModel).where(CategoryModel.is_active == True)
    )
    return result.scalars().all()


async def create_category_db(category, db: AsyncSession):
    if category.parent_id is not None:
        stmt = select(CategoryModel).where(CategoryModel.id == category.parent_id)
        result = await db.scalars(stmt)
        parent = result.first()
        if parent is None:
            raise CategoryNotFoundError()
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    await db.commit()
    return db_category


async def update_category_db(category_id: int, category, db: AsyncSession):
    stmt = select(CategoryModel).where(CategoryModel.id == category_id)
    result = await db.scalars(stmt)
    db_category = result.first()
    if not db_category:
        raise CategoryNotFoundError()

    if category.parent_id is not None:
        parent_stmt = select(CategoryModel).where(
            CategoryModel.id == category.parent_id
        )
        parent_result = await db.scalars(parent_stmt)
        parent = parent_result.first()
        if not parent:
            raise ParentCategoryNotFoundError()
        if parent.id == category_id:
            raise CategorySelfParentError()

    update_data = category.model_dump(exclude_unset=True)
    await db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(**update_data)
    )
    await db.commit()
    return db_category


async def delete_category_db(category_id: int, db: AsyncSession):
    stmt = select(CategoryModel).where(CategoryModel.id == category_id)
    result = await db.scalars(stmt)
    db_category = result.first()
    if not db_category:
        raise CategoryNotFoundError()

    await db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(is_active=False)
    )
    await db.commit()
    return db_category
