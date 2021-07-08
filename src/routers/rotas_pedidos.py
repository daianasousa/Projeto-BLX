from src.routers.auth_utils import obter_usuario_logado
from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositorio_pedidos \
    import RepositorioPedido
from src.schemas.schemas import Pedido, Usuario, PedidoSimples

router = APIRouter()


@router.post('/pedidos',
            status_code=status.HTTP_201_CREATED,
            response_model=PedidoSimples)
def fazer_pedido(
    pedido: Pedido,
    usuario: Usuario = Depends(obter_usuario_logado),
    session: Session = Depends(get_db)):
    pedido.usuario_id = usuario.id
    pedido_criado = RepositorioPedido(session).gravar_pedido(pedido)
    return pedido_criado


@router.get('/pedidos/{id}', response_model=Pedido)
def exibir_pedido(id: int, session: Session = Depends(get_db)):
    try:
        pedido = RepositorioPedido(session).buscar_por_id(id)
        return pedido
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um pedido com id={id}')


@router.get('/pedidos', response_model=List[PedidoSimples])
def listar_pedidos(usuario: Usuario = Depends(obter_usuario_logado),
                   session: Session = Depends(get_db)):
    print(usuario.id)
    pedidos = RepositorioPedido(
        session).listar_meus_pedidos_por_usuario_id(usuario.id)
    return pedidos


@router.get('/vendas', response_model=List[PedidoSimples])
def listar_vendas(usuario: Usuario = Depends(obter_usuario_logado),
                  session: Session = Depends(get_db)):
    pedidos = RepositorioPedido(
        session).listar_minhas_vendas_por_usuario_id(usuario.id)
    return pedidos