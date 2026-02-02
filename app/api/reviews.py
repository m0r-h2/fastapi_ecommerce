from fastapi import APIRouter,status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_depends import get_async_db
from app.db.models.users import User
from app.auth import get_current_admin
from app.auth import get_current_buyer
from app.schemas import Review as ReviewResponse, ReviewCreate
from app.services.reviews_crud import get_review_db, create_review_db, delete_review_db

router = APIRouter(prefix="/reviews",tags=["reviews"])



@router.get("/",response_model=list[ReviewResponse], status_code=status.HTTP_200_OK)
async def get_review(db: AsyncSession = Depends(get_async_db)):
    result = await get_review_db(db)
    return result



@router.post("/",response_model=ReviewResponse,status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate,
                        db: AsyncSession = Depends(get_async_db),
                        current_user: User = Depends(get_current_buyer)):
    result = await create_review_db(review, db, current_user.id)
    return result



@router.delete("/{review_id}",response_model=dict)
async def delete_review(review_id: int,
                        db: AsyncSession = Depends(get_async_db),
                        current_user: User = Depends(get_current_admin)):
    result = await delete_review_db(review_id, db)
    return result

