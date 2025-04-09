from pydantic import BaseModel, EmailStr, Field

class UsuarioSchema(BaseModel):
    nome: str = Field(..., min_lenght=3)
    email: EmailStr
    senha: str = Field(..., min_length=6)

class UsuarioSchemaResposta(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True

