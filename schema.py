import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Usuario(BaseModel):
    nome: str
    sobrenome: str
    email: str
    cpf: str
    adm: bool

    class Config:
        orm_mode = True


class UsuarioEdit(BaseModel):
    nome: Optional[str] = Field(None, description="Who sends the error message.")
    sobrenome: Optional[str] = Field(None, description="Who sends the error message.")
    email: Optional[str] = Field(None, description="Who sends the error message.")
    cpf: Optional[str] = Field(None, description="Who sends the error message.")
    adm: Optional[bool] = Field(None, description="Who sends the error message.")

    class Config:
        orm_mode = True


class Aeroporto(BaseModel):
    nome: str
    cidade: str
    pais: str

    class Config:
        orm_mode = True


class AeroportoEdit(BaseModel):
    nome: Optional[str] = Field(None, description="Who sends the error message.")
    cidade: Optional[str] = Field(None, description="Who sends the error message.")
    pais: Optional[str] = Field(None, description="Who sends the error message.")

    class Config:
        orm_mode = True


class Pagamento(BaseModel):
    reserva_id: int
    valor: float
    tipo: str
    status: str

    class Config:
        orm_mode = True


class Voo(BaseModel):
    origem_id: int
    destino_id: int
    data_hora_partida: datetime.datetime
    capacidade: int
    preco: float
    numero_voo: str

    class Config:
        orm_mode = True


class VooEdit(BaseModel):
    origem_id: Optional[int] = Field(None, description="Who sends the error message.")
    destino_id: Optional[int] = Field(None, description="Who sends the error message.")
    data_hora_partida: Optional[datetime.datetime] = Field(None, description="Who sends the error message.")
    capacidade: Optional[int] = Field(None, description="Who sends the error message.")
    preco: Optional[float] = Field(None, description="Who sends the error message.")
    numero_voo: Optional[str] = Field(None, description="Who sends the error message.")

    class Config:
        orm_mode = True


class Reserva(BaseModel):
    usuario_id: int
    voo_id: int
    data: datetime.datetime
    status: str

    class Config:
        orm_mode = True


class ReservaEdit(BaseModel):
    usuario_id: Optional[int] = Field(None, description="Who sends the error message.")
    voo_id: Optional[int] = Field(None, description="Who sends the error message.")
    data: Optional[datetime.datetime] = Field(None, description="Who sends the error message.")
    status: Optional[str] = Field(None, description="Who sends the error message.")

    class Config:
        orm_mode = True
