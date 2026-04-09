from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
 
 
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, example="Laptop Pro 15")
    description: Optional[str] = Field(None, example="Laptop de alto rendimiento con 16GB RAM")
    price: float = Field(..., gt=0, example=1299.99)
    stock: int = Field(..., ge=0, example=50)
    image_url: Optional[str] = Field(None, example="https://example.com/laptop.jpg")
 
    @validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return round(v, 2)
 
    @validator("stock")
    def stock_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v
 
 
class ProductCreate(ProductBase):
    pass
 
 
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
 
    @validator("price", pre=True, always=True)
    def price_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return round(v, 2) if v is not None else v
 
 
class Product(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
 
    class Config:
        from_attributes = True  # Pydantic v2 (era orm_mode en v1)