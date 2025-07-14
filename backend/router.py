from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
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
    products = get_product(db)
    return products

@router.get("/product/{product_id}", response_model=ProductResponse)
def read_one_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(product_id=product_id, db=db)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto Inexistente")

@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product, db=db)

@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = delete_product(product_id=product_id, db=db)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto Inexistente")
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
def atualizar_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product(product_id=product_id, product=product, db=db)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto Inexistente")
    return product
