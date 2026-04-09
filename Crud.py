from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
import models, schemas
 
 
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()
 
 
def get_products(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
    query = db.query(models.Product)
    if search:
        query = query.filter(
            or_(
                models.Product.name.ilike(f"%{search}%"),
                models.Product.description.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()
 
 
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
 
 
def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product is None:
        return None
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product
 
 
def delete_product(db: Session, product_id: int) -> bool:
    db_product = get_product(db, product_id)
    if db_product is None:
        return False
    db.delete(db_product)
    db.commit()
    return True