from pydantic import BaseModel
from typing import Optional, List

class ProdutoSchema(BaseModel):
    nome: str
    preco: float
    estoque: int

    class Config:
        form_atributes = True

class ProdutoSchemaResposta(ProdutoSchema):
    id: int

class ListaProdutosResposta(BaseModel):
    produtos: List[ProdutoSchemaResposta]
