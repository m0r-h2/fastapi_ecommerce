from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.users import User
from app.db.models import Review as ReviewModel
from app.db.models.products import Product as ProductModel
from app.core.exceptions import ProductUnavailableError, ReviewUnavailableError


async def update_product_rating(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()



async def get_review_db(db: AsyncSession):
    stmt = await db.execute(select(ReviewModel).where(ReviewModel.is_active == True))
    return stmt.scalars().all()



async def create_review_db(review,
                        db: AsyncSession,
                        user_id: User):

    stmt_product = await db.scalars(select(ProductModel).where(ProductModel.id == review.product_id,
                                                         ProductModel.is_active == True))
    result_product = stmt_product.first()
    if not result_product:
        raise ProductUnavailableError()

    db_review = ReviewModel(**review.model_dump(),user_id=user_id.id)
    db.add(db_review)
    await db.commit()

    await update_product_rating(db, review.product_id)

    return db_review



async def delete_review_db(review_id: int, db: AsyncSession):
    stmt_review = await db.scalars(select(ReviewModel).where(ReviewModel.id == review_id,
                                                              ReviewModel.is_active == True))
    review = stmt_review.first()
    if not review:
        raise ReviewUnavailableError()
    await db.execute(update(ReviewModel).where(ReviewModel.id == review_id).values(is_active=False))
    await db.commit()
    await db.refresh(review)

    await update_product_rating(db,review.product_id)

    return {"message": "Review deleted"}