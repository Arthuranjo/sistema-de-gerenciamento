from fastapi import HTTPException
from models.usuario_model import UsuarioSchema, UsuarioSchemaResposta
from database.conexao import conectar

def listar_usuarios():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()

        lista = []
        for usuario in usuarios:
            u = {
                "id": usuario[0],
                "nome": usuario[1],
                "email": usuario[2]
            }
            lista.append(u)

        return lista

    except Exception as e:
        print("Erro ao buscar usuários:", e)
        raise HTTPException(status_code=500, detail="Erro interno ao buscar usuários.")

def buscar_usuario(id: int):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return {
                "id": usuario[0],
                "nome": usuario[1],
                "email": usuario[2]
            }
        else:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

    except Exception as e:
        print("Erro ao buscar usuário:", e)
        raise HTTPException(status_code=500, detail="Erro interno ao buscar usuário.")


def criar_usuario(usuario: UsuarioSchema):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (usuario.email,))
        if cursor.fetchone():
            raise ValueError("E-mail já cadastrado.")

        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                       (usuario.nome, usuario.email, usuario.senha))
        conn.commit()
        return {"mensagem": "Usuário criado com sucesso"}
    except Exception as e:
        print (f"erro ao criar usuario: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def atualizar_usuario(id: int, usuario: UsuarioSchema):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET nome=%s, email=%s, senha=%s WHERE id=%s",
                       (usuario.nome, usuario.email, usuario.senha, id))
        conn.commit()
        return {"mensagem": "Usuario atualizado com sucesso"}
    finally:
        cursor.close()
        conn.close()

def deletar_usuario(id: int):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
        return {"mensagem": "Usuario deletado com sucesso"}
    finally:
        cursor.close()
        conn.close()

        