from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from fastapi_cache.key_builder import default_key_builder

from app.core.config import settings
from app.services.categories_crud import (
    get_all_categories_db,
    create_category_db,
    update_category_db,
    delete_category_db,
)
from app.schemas import Category as CategorySchema, CategoryCreate

from sqlalchemy.ext.asyncio import AsyncSession
from app.db_depends import get_async_db

router = APIRouter(
    prefix="/categories",
    tags=["category"],
)


@router.get("/", response_model=list[CategorySchema], status_code=status.HTTP_200_OK)
@cache(
    expire=60,
    namespace=settings.cache.namespace.category_list,
)
async def get_all_categories(db: AsyncSession = Depends(get_async_db)):
    result = await get_all_categories_db(db)
    return result


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate, db: AsyncSession = Depends(get_async_db)
):
    result = await create_category_db(category=category, db=db)
    return result


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: int, category: CategoryCreate, db: AsyncSession = Depends(get_async_db)
):
    result = await update_category_db(category_id, category, db)
    return result


@router.delete("/{category_id}", response_model=CategorySchema)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await delete_category_db(category_id, db)
    return result
