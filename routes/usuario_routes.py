from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from models.usuario_model import UsuarioSchema, UsuarioSchemaResposta
from controllers import usuario_controller

router = APIRouter(prefix="/usuarios", tags=["Usuários"])
templates = Jinja2Templates(directory="templates")


@router.get("/formulario", response_class=HTMLResponse)
def formulario_usuario(request: Request):
    return templates.TemplateResponse("usuarios/formulario.html", {
        "request": request,
        "erros": [],
        "nome": "",
        "email": "",
        "senha": ""
    })


@router.post("/formulario", response_class=HTMLResponse)
def criar_usuario_formulario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...)
):
    try:
        usuario = UsuarioSchema(nome=nome, email=email, senha=senha)
        usuario_controller.criar_usuario(usuario)
        return RedirectResponse(url="/usuarios/pagina", status_code=303)

    except ValidationError as e:
        erros = e.errors()
        return templates.TemplateResponse("usuarios/formulario.html", {
            "request": request,
            "erros": erros,
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


@router.post("/deletar", response_class=HTMLResponse)
def deletar_usuario_formulario(request: Request, id: int = Form(...)):
    usuario_controller.deletar_usuario(id)
    return RedirectResponse(url="/usuarios/pagina", status_code=303)


@router.get("/", response_model=list[UsuarioSchemaResposta])
def get_usuarios():
    return usuario_controller.listar_usuarios()


@router.get("/{id}", response_model=UsuarioSchemaResposta)
def get_usuario(id: int):
    return usuario_controller.buscar_usuario(id)


@router.post("/")
def post_usuario(usuario: UsuarioSchema):
    return usuario_controller.criar_usuario(usuario)


@router.put("/{id}")
def put_usuario(id: int, usuario: UsuarioSchema):
    return usuario_controller.atualizar_usuario(id, usuario)


@router.delete("/{id}")
def deletar_usuario(id: int):
    return usuario_controller.deletar_usuario(id)

