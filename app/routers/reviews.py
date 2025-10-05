from fastapi import APIRouter,status,HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_depends import get_async_db
from sqlalchemy import select, update
from sqlalchemy.sql import func
from app.models.users import User
from app.auth import get_current_admin
from app.auth import get_current_buyer
from app.models.reviews import Review as ReviewModel
from app.schemas import Review as ReviewResponse, ReviewCreate
from app.models.products import Product as ProductModel

router = APIRouter(prefix="/reviews",tags=["reviews"])


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


@router.get("/",response_model=list[ReviewResponse], status_code=status.HTTP_200_OK)
async def get_review(db: AsyncSession = Depends(get_async_db)):
    stmt = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    return stmt.all()



@router.post("/",response_model=ReviewResponse,status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate,
                        db: AsyncSession = Depends(get_async_db),
                        current_user: User = Depends(get_current_buyer)):

    stmt_product = await db.scalars(select(ProductModel).where(ProductModel.id == review.product_id,
                                                         ProductModel.is_active == True))
    result_product = stmt_product.first()
    if not result_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не существует или неактивен")

    db_review = ReviewModel(**review.model_dump(),user_id=current_user.id)
    db.add(db_review)
    await db.commit()
    return db_review


@router.delete("/{review_id}",response_model=dict)
async def delete_review(review_id: int,
                        db: AsyncSession = Depends(get_async_db),
                        current_user: User = Depends(get_current_admin)):
    stmt_review = await db.scalars(select(ReviewModel).where(ReviewModel.id == review_id,
                                                              ReviewModel.is_active == True))
    review = stmt_review.first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Коменнтарий не существует или неактивен")
    if current_user:
        pass
    await db.execute(update(ReviewModel).where(ReviewModel.id == review_id).values(is_active=False))
    await db.commit()
    await db.refresh(review)

    update_product_rating(db,review.product_id)

    return {"message": "Review deleted"}

