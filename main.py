from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, crud
from database import SessionLocal, engine
 
models.Base.metadata.create_all(bind=engine)
 
app = FastAPI(
    title="Ecommerce API",
    description="API REST para gestión de productos con FastAPI + Amazon RDS",
    version="1.0.0"
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar el dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 
@app.get("/", tags=["Health"])
def root():
    return {"message": "Ecommerce API funcionando correctamente", "docs": "/docs"}
 
 
@app.post("/products", response_model=schemas.Product, status_code=201, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Crear un nuevo producto."""
    return crud.create_product(db=db, product=product)
 
 
@app.get("/products", response_model=List[schemas.Product], tags=["Products"])
def list_products(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Listar todos los productos. Soporta paginación y búsqueda por nombre."""
    return crud.get_products(db=db, skip=skip, limit=limit, search=search)
 
 
@app.get("/products/{product_id}", response_model=schemas.Product, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Obtener un producto por ID."""
    product = crud.get_product(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Producto con ID {product_id} no encontrado")
    return product
 
 
@app.put("/products/{product_id}", response_model=schemas.Product, tags=["Products"])
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """Actualizar nombre, descripción, precio o stock de un producto."""
    updated = crud.update_product(db=db, product_id=product_id, product=product)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Producto con ID {product_id} no encontrado")
    return updated
 
 
@app.delete("/products/{product_id}", status_code=204, tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Eliminar un producto por ID."""
    deleted = crud.delete_product(db=db, product_id=product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Producto con ID {product_id} no encontrado")
    return None
 