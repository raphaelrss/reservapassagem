import re
from pydantic import validator
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    sobrenome = Column(String)
    email = Column(String)
    cpf = Column(String)
    hash_password = Column(String)
    adm = Column(Boolean)

    @validator('email')
    def valida_formatacao_email(cls, v):
        if not re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+').match(v):
            raise ValueError('The user email format is invalid!')
        return v


class Aeroporto(Base):
    __tablename__ = "aeroporto"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cidade = Column(String)
    pais = Column(String)


class Pagamento(Base):
    __tablename__ = "pagamento"
    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reserva.id"))
    valor = Column(Float)
    tipo = Column(String)
    status = Column(String)

    reserva = relationship("Reserva")


class Voo(Base):
    __tablename__ = "voo"
    id = Column(Integer, primary_key=True, index=True)
    origem_id = Column(Integer, ForeignKey("aeroporto.id"))
    destino_id = Column(Integer, ForeignKey("aeroporto.id"))
    data_hora_partida = Column(DateTime(timezone=True))
    capacidade = Column(Integer)
    preco = Column(Float)
    numero_voo = Column(String)

    origem = relationship("Aeroporto", primaryjoin="Voo.origem_id == foreign(Aeroporto.id)")
    destino = relationship("Aeroporto", primaryjoin="Voo.destino_id == foreign(Aeroporto.id)")


class Reserva(Base):
    __tablename__ = "reserva"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("reserva.id"))
    voo_id = Column(Integer, ForeignKey("voo.id"))
    data = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String)

    usuario = relationship("Usuario", primaryjoin="foreign(Reserva.usuario_id) == Usuario.id")
    voo = relationship("Voo")

