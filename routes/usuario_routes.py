from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from models.usuario_model import UsuarioSchema, UsuarioSchemaResposta
from controllers import usuario_controller

router = APIRouter(prefix="/usuarios", tags=["Usuários"])
templates = Jinja2Templates(directory="templates")

# -------------------------
# FORMULÁRIOS HTML (JINJA2)
# -------------------------

@router.get("/", response_class=HTMLResponse)
async def pagina_inicial(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/formulario", response_class=HTMLResponse)
def formulario_usuario(request: Request):
    return templates.TemplateResponse("usuarios/formulario.html", {
        "request": request,
        "erros": [],
        "id": "",
        "nome": "",
        "email": "",
        "senha": ""
    })


@router.get("/formulario_editar/{id}", response_class=HTMLResponse)
def exibir_formulario_edicao(request: Request, id: int):
    usuario = usuario_controller.buscar_usuario(id)

    if not usuario:
        return templates.TemplateResponse("erro.html", {
            "request": request,
            "mensagem": f"Usuário com id {id} não encontrado."
        })

    print("DEBUG:", usuario, type(usuario))  # isso vai ajudar a saber se é dict, Row, etc.

    return templates.TemplateResponse("usuarios/formulario.html", {
        "request": request,
        "id": usuario["id"],        # <= use colchetes aqui
        "nome": usuario["nome"],
        "email": usuario["email"],
        "senha": ""
    })


@router.post("/formulario", response_class=HTMLResponse)
def criar_ou_editar_usuario_formulario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    id: int = Form(None)
):
    try:
        usuario = UsuarioSchema(nome=nome, email=email, senha=senha)

        if id:
            usuario_controller.atualizar_usuario(id, usuario)
        else:
            usuario_controller.criar_usuario(usuario)

        return RedirectResponse(url="/usuarios/pagina", status_code=303)

    except ValidationError as e:
        erros = e.errors()
        return templates.TemplateResponse("usuarios/formulario.html", {
            "request": request,
            "erros": erros,
            "id": id,
            "nome": nome,
            "email": email,
            "senha": senha
        })


@router.get("/pagina", response_class=HTMLResponse)
def listar_usuarios_html(request: Request):
    usuarios = usuario_controller.listar_usuarios()
    return templates.TemplateResponse("usuarios/listar.html", {
        "request": request,
        "usuarios": usuarios
    })


@router.post("/deletar/{id}", response_class=HTMLResponse)
def deletar_usuario_formulario(id: int):
    usuario_controller.deletar_usuario(id)
    return RedirectResponse(url="/usuarios/pagina", status_code=303)

# -------------------------
# API RESTful
# -------------------------

@router.get("/", response_model=list[UsuarioSchemaResposta])
def get_usuarios():
    return usuario_controller.listar_usuarios()

@router.post("/")
def post_usuario(usuario: UsuarioSchema):
    return usuario_controller.criar_usuario(usuario)

@router.put("/{id}")
def put_usuario(id: int, usuario: UsuarioSchema):
    return usuario_controller.atualizar_usuario(id, usuario)

@router.delete("/{id}")
def deletar_usuario(id: int):
    return usuario_controller.deletar_usuario(id)

# -------------------------
# ROTA GENÉRICA (DEIXAR POR ÚLTIMO)
# -------------------------

@router.get("/{id}", response_model=UsuarioSchemaResposta)
def get_usuario(id: int):
    return usuario_controller.buscar_usuario(id)


