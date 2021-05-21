from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.schemas.schemas import Pedido, PedidoSimples
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositorio_pedidos import RepositorioPedido


router = APIRouter()


@router.post('/pedidos', status_code=status.HTTP_201_CREATED, response_model=Pedido)
def fazer_pedido(pedido: Pedido, session: Session = Depends(get_db)):
    pedido_criado = RepositorioPedido(session).gravar_pedido(pedido)
    return pedido_criado


@router.get('/pedidos/{id}', response_model=List[Pedido])
def exibir_pedido(id: int, session: Session = Depends(get_db)):
    pedido = RepositorioPedido(session).buscar_por_id(id)
    if not pedido:
        raise HTTPException(status_code=404, detail=f"ID  não foi localizado!")
    return pedido


@router.get('/pedidos', status_code=status.HTTP_200_OK, response_model=List[Pedido])
def listar(session: Session = Depends(get_db)):
    pedidos  = RepositorioPedido(session).listar()
    return pedidos


@router.get('/pedidos/{usuario_id}/pedidos', response_model=List[PedidoSimples])
def listar_pedidos(usuario_id: int, session: Session = Depends(get_db)):
    pedidos = RepositorioPedido(session).listar_meus_pedidos_por_usuario_id(usuario_id)

    if not pedidos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não há um usuário com o id {usuario_id}')

    return pedidos

@router.get('/pedidos/{usuario_id}/vendas', response_model=List[PedidoSimples])
def listar_vendas(usuario_id: int, session: Session = Depends(get_db)):
    pedidos = RepositorioPedido(session).listar_minhas_vendas_por_usuario_id(usuario_id)

    if not pedidos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não há um usuário com o id {usuario_id}')

    return pedidos