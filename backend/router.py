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
