from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_seller
from app.db.models.users import User as UserModel
from app.schemas import Product as ProductSchema, ProductCreate
from app.schemas import Review as ReviewResponse
from app.db_depends import get_async_db
from app.services.products_crud import (
    get_all_products_db,
    create_product_db,
    get_products_by_category_db,
    get_product_db,
    update_product_db,
    delete_product_db,
    get_product_id_reviews_db,
)

from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_all_products(db: AsyncSession = Depends(get_async_db)):
    result = await get_all_products_db(db=db)
    return result


@router.get(
    "/category/{category_id}",
    response_model=list[ProductSchema],
    status_code=status.HTTP_200_OK,
)
async def get_products_by_category(
    category_id: int, db: AsyncSession = Depends(get_async_db)
):
    result = await get_products_by_category_db(category_id, db)
    return result


@router.get(
    "/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK
)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await get_product_db(product_id, db)
    return result


@router.get(
    "/{product_id}/reviews/",
    response_model=list[ReviewResponse],
    status_code=status.HTTP_200_OK,
)
async def get_product_id_reviews(
    product_id: int, db: AsyncSession = Depends(get_async_db)
):
    result = await get_product_id_reviews_db(product_id, db)
    return result


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_seller),
):
    result = await create_product_db(product=product, seller_id=current_user.id, db=db)
    return result


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product: ProductCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_seller),
):
    result = await update_product_db(product_id, product, db, user_id=current_user.id)
    return result


@router.delete(
    "/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_seller),
):
    result = await delete_product_db(product_id, db, user_id=current_user.id)
    return result
