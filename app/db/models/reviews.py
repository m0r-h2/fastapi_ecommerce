from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Integer,Text,DateTime,Boolean
from datetime import datetime

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer,primary_key=True, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id",ondelete="CASCADE"), nullable=False)

    comment: Mapped[str] = mapped_column(Text, nullable=True)
    comment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now,nullable=False)
    grade: Mapped[int] = mapped_column(Integer,nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
