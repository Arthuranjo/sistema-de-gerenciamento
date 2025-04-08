import _mysql_connector
from fastapi import HTTPException
from database.conexao import conectar
from models.produto_model import ProdutoSchema

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def buscar_produto_por_id(produto_id: int):
    conn = conectar()
    cursor = conn.cursor
    cursor.execute("SELECT * FROM produto WHERE id = %s", (produto_id))
    produto = cursor.fetchone()
    conn.close()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

def criar_produto(produto: ProdutoSchema):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (%s, %s, %s)",
                   (produto.nome, produto.preco, produto.estoque))
    conn.commit()
    conn.close()
    return {"mensagem": "Produto criado com sucesso"}