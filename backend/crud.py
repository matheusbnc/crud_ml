"""Operações CRUD para o modelo ProductModel."""

from sqlalchemy.orm import Session
from schema import ProductUpdate, ProductCreate
from models import ProductModel

def get_products(db: Session):
    """Retorna todos os produtos do banco de dados.

    Args:
        db (Session): Sessão do banco de dados.

    Returns:
        list: Lista de instâncias ProductModel.
    """
    return db.query(ProductModel).all()

def get_product(db: Session, product_id: int):
    """Retorna um produto pelo ID.

    Args:
        db (Session): Sessão do banco de dados.
        product_id (int): ID do produto.

    Returns:
        ProductModel or None: Produto encontrado ou None.
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

def create_product(db: Session, product: ProductCreate):
    """Cria um novo produto no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        product (ProductCreate): Dados do produto.

    Returns:
        ProductModel: Produto criado.
    """
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    """Remove um produto pelo ID.

    Args:
        db (Session): Sessão do banco de dados.
        product_id (int): ID do produto.

    Returns:
        ProductModel or None: Produto removido ou None.
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate):
    """Atualiza os dados de um produto.

    Args:
        db (Session): Sessão do banco de dados.
        product_id (int): ID do produto.
        product (ProductUpdate): Dados para atualização.

    Returns:
        ProductModel or None: Produto atualizado ou None.
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if db_product is None:
        return None
    
    if product.name is not None:
        db_product.name = product.name
    
    if product.description is not None:
        db_product.description = product.description
    
    if product.price is not None:
        db_product.price = product.price

    if product.category is not None:
        db_product.category = product.category
    
    if product.supplier_email is not None:
        db_product.supplier_email = product.supplier_email

    db.commit()
    db.refresh(db_product)
    return db_product
