from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select
from sqlalchemy.sql.functions import mode
from src.schemas import schemas
from src.infra.sqlalchemy.models import models


class RepositorioPedido():
    def __init__(self, session: Session): 
        self.session = session


    def gravar_pedido(self, pedido: schemas.Pedido):
        db_pedidos = models.Pedido(quantidade=pedido.quantidade,
                                    local_entrega=pedido.local_entrega,
                                    tipo_entrega=pedido.tipo_entrega,
                                    observacao=pedido.observacao,
                                    usuario_id=pedido.usuario_id,
                                    produto_id=pedido.produto_id)

        self.session.add(db_pedidos)
        self.session.commit()
        self.session.refresh(db_pedidos)
        return db_pedidos


    def buscar_por_id(self, id: int):
        consulta = select(models.Pedido).where(models.Pedido.id == id)
        pedido = self.session.execute(consulta).scalars().all()
        return pedido


    def listar(self):
        pedidos = self.session.query(models.Pedido).all()
        return pedidos


    def listar_meus_pedidos_por_usuario_id(self, usuario_id: int):
        usuario = select(models.Pedido).where(models.Pedido.usuario_id == usuario_id)
        meus_pedidos = self.session.execute(usuario).scalars().all()
        return meus_pedidos


    def listar_minhas_vendas_por_usuario_id(self, usuario_id: int):
        usuario = select(models.Pedido).join_from(models.Pedido, models.Produto).where(models.Produto.usuario_id == usuario_id)
        minhas_vendas = self.session.execute(usuario).scalars().all()
        return minhas_vendas