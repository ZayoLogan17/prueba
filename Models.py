from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from database import Base
 
 
class Product(Base):
    """
    Modelo de Producto para tienda de vinilos.
    El campo 'name' se usa como "Artista — Álbum" (ej: "Pink Floyd — The Wall").
    El campo 'description' puede incluir género, año, sello discográfico, etc.
    El campo 'image_url' almacena la URL de la portada del disco.
    """
    __tablename__ = "products"
 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)   # Formato: "Artista — Álbum"
    description = Column(Text, nullable=True)                # Género, año, edición, sello
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    image_url = Column(String(500), nullable=True)           # URL de portada del vinilo
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 