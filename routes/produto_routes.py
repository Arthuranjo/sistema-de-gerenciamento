from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from models.produto_model import ProdutoSchema, ProdutoSchemaResposta
from controllers import produto_controller

router = APIRouter(prefix="/produtos", tags=["Produtos"])
templates = Jinja2Templates(directory="templates")


@router.get("/formulario", response_class=HTMLResponse)
def exibir_formulario(request: Request):
    return templates.TemplateResponse("produtos/formulario.html", {"request": request})

@router.post("/formulario", response_class=HTMLResponse)
def criar_via_formulario(
    request: Request,
    nome: str = Form(...),
    preco: float = Form(...),
    estoque: int = Form(...)
):
    if len(nome) < 3 or preco <= 0 or estoque < 0:
        return templates.TemplateResponse("produtos/formulario.html", {
            "request": request,
            "erro": "Dados inválidos! Verifique os campos.",
            "nome": nome,
            "preco": preco,
            "estoque": estoque
        })

    produto = ProdutoSchema(nome=nome, preco=preco, estoque=estoque)
    produto_controller.criar_produto(produto)
    return RedirectResponse(url="/produtos/pagina", status_code=303)

@router.get("/pagina", response_class=HTMLResponse)
def pagina_listagem(request: Request):
    produtos = produto_controller.listar_produtos()
    return templates.TemplateResponse("produtos/listar.html", {"request": request, "produtos": produtos})

@router.get("/formulario_editar/{produto_id}", response_class=HTMLResponse)
def exibir_formulario_edicao(request: Request, produto_id: int):
    produto = produto_controller.buscar_produto_por_id(produto_id)
    return templates.TemplateResponse("produtos/editar.html", {"request": request, "produto": produto})

@router.post("/formulario_editar/{produto_id}", response_class=HTMLResponse)
def editar_produto(
    request: Request,
    produto_id: int,
    nome: str = Form(...),
    preco: float = Form(...),
    estoque: int = Form(...)
):
    if len(nome) < 3 or preco <= 0 or estoque < 0:
        return templates.TemplateResponse("produtos/editar.html", {
            "request": request,
            "erro": "Dados inválidos! Verifique os campos.",
            "produto": {"id": produto_id, "nome": nome, "preco": preco, "estoque": estoque}
        })

    produto = ProdutoSchema(nome=nome, preco=preco, estoque=estoque)
    produto_controller.atualizar_produto(produto_id, produto)
    return RedirectResponse(url="/produtos/pagina", status_code=303)

@router.get("/", response_model=list[ProdutoSchemaResposta])
def listar():
    return produto_controller.listar_produtos()

@router.post("/")
def criar(produto: ProdutoSchema):
    return produto_controller.criar_produto(produto)

@router.put("/{produto_id}")
def atualizar(produto_id: int, produto: ProdutoSchema):
    return produto_controller.atualizar_produto(produto_id, produto)

@router.delete("/{produto_id}")
def deletar(produto_id: int):
    return produto_controller.deletar_produto(produto_id)


@router.post("/deletar/{produto_id}")
def excluir_produto(produto_id: int):
    produto_controller.deletar_produto(produto_id)
    return RedirectResponse(url="/produtos/pagina", status_code=303)

@router.get("/{produto_id}", response_model=ProdutoSchemaResposta)
def buscar(produto_id: int):
    return produto_controller.buscar_produto_por_id(produto_id)

