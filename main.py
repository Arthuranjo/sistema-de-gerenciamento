from database.conexao import conectar

try:
    db = conectar()
    print("Conexão realizada com sucesso!")
    db.close()
except Exception as e:
    print(f"Erro ao conectar: {e}")
