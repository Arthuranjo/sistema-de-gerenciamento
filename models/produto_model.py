from pydantic import BaseModel, Field, validator

class ProdutoSchema(BaseModel):
    nome: str = Field(..., min_length=3)
    preco: float = Field(..., gt=0)
    estoque: int = Field(... ,ge=0)

    @validator('nome')
    def nome_minimo(cls, v):
        if len(v) < 3:
            raise ValueError('O nome do produto deve conter no minimo 3 letras')
        return v
    
    class ProdutosSchemaResposta(ProdutoSchema):
        id: int

        class Config:
            orm_mode = True