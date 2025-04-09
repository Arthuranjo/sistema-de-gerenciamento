# sistema-de-gerenciamento
Este projeto é uma aplicação web desenvolvida com **FastAPI**, utilizando o padrão **MVC (Model-View-Controller)** e banco de dados **MySQL**. O sistema permite o gerenciamento completo de produtos e usuários com operações CRUD, além de páginas HTML para interação visual com formulários.

---

## Estrutura
- **Model**: Define os esquemas dos dados (validação).
- **View**: Templates HTML com formulários e exibição de dados.
- **Controller**: Regras de negócio e integração com o banco de dados.
- **Routes**: Define os endpoints e liga as camadas.

---

## Funcionalidades

### Produtos

#### Regras de validação
- O nome do produto deve ter **mínimo 3 caracteres**.
- O preço deve ser um **valor positivo**.
- O estoque deve ser um **número inteiro ≥ 0**.

#### Endpoints
| Método | Rota                     | Descrição                                     |
|--------|--------------------------|-----------------------------------------------|
| GET    | `/produtos`              | Retorna todos os produtos.                    |
| GET    | `/produtos/{id}`         | Retorna um produto específico por ID.         |
| POST   | `/produtos`              | Cria um novo produto (com validação).         |
| PUT    | `/produtos/{id}`         | Atualiza os dados de um produto (com validação). |
| DELETE | `/produtos/{id}`         | Exclui um produto com base no ID.             |

### Usuários

#### Endpoints
| Método | Rota                     | Descrição                                     |
|--------|--------------------------|-----------------------------------------------|
| GET    | `/usuarios`              | Retorna todos os usuários.                    |
| GET    | `/usuarios/{id}`         | Retorna um usuário específico por ID.         |
| POST   | `/usuarios`              | Cria um novo usuário (com validação).         |
| PUT    | `/usuarios/{id}`         | Atualiza os dados de um usuário (com validação). |
| DELETE | `/usuarios/{id}`         | Exclui um usuário com base no ID.             |



---

## Front-end

O projeto inclui páginas HTML com formulários para cadastrar, editar e listar produtos e usuários, com validação básica dos campos.

---

## Tecnologias utilizadas

- Python 3.11+
- FastAPI
- MySQL
- mysql-connector-python
- HTML5 / CSS3
- Jinja2 (para templates HTML)

---

## Executando o projeto

1. repositório:
  https://github.com/Arthuranjo/sistema-de-gerenciamento#
