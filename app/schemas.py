from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50,
                      description="Название категории (3-50 символов)")
    parent_id: Optional[int] = Field(None, description="ID родительской категории, если есть")


class Category(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор категории")
    name: str = Field(..., description="Название категории")
    parent_id: Optional[int] = Field(None, description="ID родительской категории, если есть")
    is_active: bool = Field(..., description="Активность категории")

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100,
                      description="Название товара (3-100 символов)")
    description: Optional[str] = Field(None, max_length=500,
                                       description="Описание товара (до 500 символов)")
    price: float = Field(..., gt=0, description="Цена товара (больше 0)")
    image_url: Optional[str] = Field(None, max_length=200, description="URL изображения товара")
    stock: int = Field(..., ge=0, description="Количество товара на складе (0 или больше)")
    category_id: int = Field(..., description="ID категории, к которой относится товар")


class Product(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор товара")
    name: str = Field(..., description="Название товара")
    description: Optional[str] = Field(None, description="Описание товара")
    price: float = Field(..., description="Цена товара")
    image_url: Optional[str] = Field(None, description="URL изображения товара")
    stock: int = Field(..., description="Количество товара на складе")
    category_id: int = Field(..., description="ID категории")
    is_active: bool = Field(..., description="Активность товара")
    rating: float = Field(...,description="Средний рейтинг")
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(max_length=8,description="Пароль (минимум 8 символов)")
    role: str = Field(default="buyer",pattern="^(buyer|seller)$", description="Роль: 'buyer' или 'seller'")

class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str
    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    product_id: int = Field(..., description="ID продукта")
    comment: Optional[str] = Field(None, description="Комментарий пользователя")
    grade: int = Field(...,ge=1,le=5, description="Оценка от 1 до 5")

class Review(BaseModel):
    id: int
    user_id: int
    product_id: int
    comment: Optional[str]
    comment_date: datetime
    grade: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)