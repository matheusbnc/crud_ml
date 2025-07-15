"""Schemas Pydantic para validação e serialização de produtos."""

from pydantic import BaseModel, PositiveFloat, EmailStr, model_validator
from enum import Enum
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    """Base para schemas de produto."""
    name: str
    description: str
    price: PositiveFloat
    category: str
    supplier_email: EmailStr

class ProductCreate(ProductBase):
    """Schema para criação de produto."""
    pass

class ProductResponse(ProductBase):
    """Schema de resposta para produto."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    """Schema para atualização parcial de produto."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None
    category: Optional[str] = None
    supplier_email: Optional[EmailStr] = None
