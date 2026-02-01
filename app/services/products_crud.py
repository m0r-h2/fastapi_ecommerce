from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Product as ProductModel, Category as CategoryModel, Review as ReviewModel



async def get_all_products_db(db: AsyncSession):
    result = await db.execute(select(ProductModel).where(ProductModel.is_active == True))
    return result.scalars().all()


async def create_product_db(product, seller_id: int ,db: AsyncSession):
    category_result = await db.scalars(
            select(CategoryModel).where(CategoryModel.id == product.category_id,
                                        CategoryModel.is_active == True))
    if not category_result.first():
        return 3

    db_product = ProductModel(**product.model_dump(), seller_id=seller_id)
    db.add(db_product)
    await db.commit()
    return db_product



async def get_products_by_category_db(category_id: int, db: AsyncSession):
    category_result = await db.scalars(
        select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active == True)
    )
    category = category_result.first()
    if not category:
        return 3
    product_result = await db.execute(
        select(ProductModel).where(ProductModel.category_id == category_id, ProductModel.is_active == True)
    )
    return product_result.scalars().all()



async def get_product_db(product_id: int, db: AsyncSession):
    result = await db.scalars(
        select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    )
    product = result.first()
    if not product:
        return 3
    return product



async def get_product_id_reviews_db(product_id: int, db: AsyncSession):
    stmt_product = await db.scalars(select(ProductModel).where(ProductModel.id == product_id,
                                           ProductModel.is_active == True))
    product = stmt_product.first()
    if not product:
        return 3

    result = await db.execute(select(ReviewModel).where(ReviewModel.product_id == product_id,
                                          ReviewModel.is_active == True))
    return result.scalars().all()



async def update_product_db(product_id: int, product, db: AsyncSession, user_id: int):
    result = await db.scalars(select(ProductModel).where(ProductModel.id == product_id))
    db_product = result.first()
    if not db_product:
        return 3
    if db_product.seller_id != user_id:
        return 4
    category_result = await db.scalars(
        select(CategoryModel).where(CategoryModel.id == product.category_id, CategoryModel.is_active == True)
    )
    if not category_result.first():
        return 5
    await db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(**product.model_dump())
    )
    await db.commit()
    await db.refresh(db_product)
    return db_product



async def delete_product_db(product_id: int, db: AsyncSession, user_id: int):
    result = await db.scalars(
        select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    )
    product = result.first()
    if not product:
        return 3
    if product.seller_id != user_id:
        return 4
    await db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(is_active=False)
    )
    await db.commit()
    await db.refresh(product)
    return product