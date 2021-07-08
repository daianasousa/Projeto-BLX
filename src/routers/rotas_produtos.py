from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.schemas.schemas import Produto, ProdutoSimples, Usuario
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositorio_produto \
    import RepositorioProduto
from src.routers.auth_utils import obter_usuario_logado

router = APIRouter()

#Cadastrar Produtos
@router.post('/produtos',
            status_code=status.HTTP_201_CREATED,
            response_model=ProdutoSimples)
def criar_produto(
    produto: Produto,
    usuario: Usuario = Depends(obter_usuario_logado),
    db: Session = Depends(get_db)):
    produto.usuario_id = usuario.id
    produto_criado = RepositorioProduto(db).criar(produto)
    return produto_criado

#Listar Produtos Cadastrados
@router.get('/produtos', response_model=List[ProdutoSimples])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = RepositorioProduto(db).listar()
    return produtos
    
@router.get('/produtos/{id}')
def exibir_produto(id: int, session: Session = Depends(get_db)):
    produto_localizado = RepositorioProduto(session).buscarPorId(id)
    if not produto_localizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Não há um produto com o id = {id}')
    return produto_localizado

@router.put('/produtos/{id}', response_model=ProdutoSimples)
def atualizar_produto(
        id: int,
        produto: Produto,
        usuario: Usuario = Depends(obter_usuario_logado),
        session: Session = Depends(get_db)):
    produto.usuario_id = usuario.id
    RepositorioProduto(session).editar(id, produto)
    produto.id = id
    return produto


@router.delete('/produtos/{id}')
def remover_produto(id: int, 
    session: Session = Depends(get_db)):
    excluir = RepositorioProduto(session).remover(id)
    if not excluir:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto por ID {id} não localizado!")
    return excluir