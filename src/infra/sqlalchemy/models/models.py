from sqlalchemy import Column, Integer, String, Float, Boolean
from src.infra.sqlalchemy.config.database import Base

class Produto(Base):
    __tablename__ = 'produto'

    id = Column(Integer, primary_key=True, index=False)
    nome = Column(String)
    preco = Column(Float)
    detalhes = Column(String)
    disponivel = Column(Boolean)