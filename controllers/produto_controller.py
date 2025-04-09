import mysql.connector
from fastapi import HTTPException
from database.conexao import conectar
from models.produto_model import ProdutoSchema

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    resultados = cursor.fetchall()
    conn.close()

    produtos = []
    for linha in resultados:
        produto = {
            "id": linha[0],
            "nome": linha[1],
            "preco": float(linha[2]),
            "estoque": linha[3]
        }
        produtos.append(produto)

    return produtos


def buscar_produto_por_id(produto_id: int):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (produto_id,))
    linha = cursor.fetchone()
    conn.close()

    if not linha:
        raise HTTPException(status_code=404, detail="Produto não encontrado")


    produto = {
        "id": linha[0],
        "nome": linha[1],
        "preco": float(linha[2]),
        "estoque": linha[3]
    }

    return produto


def criar_produto(produto: ProdutoSchema):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (%s, %s, %s)",
                   (produto.nome, produto.preco, produto.estoque))
    conn.commit()
    conn.close()
    return {"mensagem": "Produto criado com sucesso"}

def atualizar_produto(produto_id: int, produto: ProdutoSchema):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET nome = %s, preco = %s, estoque = %s WHERE id = %s",
                   (produto.nome, produto.preco, produto.estoque, produto_id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    conn.commit()
    conn.close()
    return {"mensagem": "Produto atualizado com sucesso"}

def deletar_produto(produto_id: int):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = %s", 
                   (produto_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    conn.commit()
    conn.close()
    return {"mensagem": "Produto deletado com sucesso"}
