"""Rotas da API para operações CRUD de produtos."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schema import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product
)

router = APIRouter()

@router.get("/product/", response_model=List[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    """Lista todos os produtos."""
    products = get_products(db)
    return products

@router.get("/product/{product_id}", response_model=ProductResponse)
def read_one_product(product_id: int, db: Session = Depends(get_db)):
    """Obtém um produto pelo ID."""
    product = get_product(product_id=product_id, db=db)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto Inexistente")
    return product

@router.post("/products/", response_model=ProductResponse)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    """Cria um novo produto."""
    return create_product(db=db, product=product)

@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    """Remove um produto pelo ID."""
    product = delete_product(product_id=product_id, db=db)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto Inexistente")
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_route(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """Atualiza um produto pelo ID."""
    product = update_product(product_id=product_id, product=product, db=db)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto Inexistente")
    return product
