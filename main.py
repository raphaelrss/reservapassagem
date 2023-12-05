import os
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from depends import get_usuario_logado

from models import Usuario, Aeroporto, Pagamento, Voo, Reserva
from schema import UsuarioCreateRequest, Usuario as UsuarioSchema, Aeroporto as AeroportoSchema, Pagamento as PagamentoSchema, UsuarioResponse, UsuarioUpdateRequest, Voo as VooSchema, Reserva as ReservaSchema
from schema import UsuarioEdit as UsuarioEditSchema, AeroportoEdit as AeroportoEditSchema, VooEdit as VooEditSchema, ReservaEdit as ReservaEditSchema
from security import criar_token_jwt, verify_password

from fastapi.middleware.cors import CORSMiddleware


load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://reservas-de-passagens.biancacordeiro1.repl.co"],
    allow_credentials=True,
    allow_methods=["https://reservas-de-passagens.biancacordeiro1.repl.co"],
    allow_headers=["https://reservas-de-passagens.biancacordeiro1.repl.co"],
)


@app.get("/")
async def root():
    return {"message": "Bem vindo ao Fly Reservas!"}


@app.get("/usuarios/", response_model=List[UsuarioResponse])
async def usuarios():
    usuarios = db.session.query(Usuario).all()
    return usuarios


@app.post("/usuarios/create/", response_model=UsuarioResponse)
async def create_usuario(usuario: UsuarioCreateRequest):
    atributos = usuario.model_dump(exclude_unset=True)
    db_usuario = Usuario(**atributos)
    db.session.add(db_usuario)
    db.session.commit()
    return db_usuario


@app.put("/usuarios/edit/{usuario_id}/", response_model=UsuarioResponse)
async def edit_usuario(usuario_id: int, usuario: UsuarioUpdateRequest, ):
    db_usuario = db.session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    for field, value in usuario.model_dump(exclude_unset=True).items():
        setattr(db_usuario, field, value)

    db.session.commit()
    db.session.refresh(db_usuario)

    return db_usuario


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    db_usuario = db.session.query(Usuario).filter(Usuario.email == username).first()
    if not db_usuario or not verify_password(password, db_usuario.hash_password):
        raise HTTPException(status_code=403,
                            detail="Email ou nome de usuário incorretos"
                           )
    return {
        "access_token": criar_token_jwt(db_usuario.id),
        "token_type": "bearer",
    }


@app.get("/aeroportos/")
async def aeroportos():
    aeroportos = db.session.query(Aeroporto).all()
    return aeroportos


@app.post("/aeroportos/create/", response_model=AeroportoSchema)
async def create_aeroporto(aeroporto: AeroportoSchema):
    db_aeroporto = Aeroporto(nome=aeroporto.nome, cidade=aeroporto.cidade, pais=aeroporto.pais)
    db.session.add(db_aeroporto)
    db.session.commit()
    return db_aeroporto


@app.put("/aeroportos/edit/{aeroporto_id}/", response_model=AeroportoEditSchema)
async def edit_aeroporto(aeroporto_id: int, aeroporto: AeroportoEditSchema):
    db_aeroporto = db.session.query(Aeroporto).filter(Aeroporto.id == aeroporto_id).first()
    if db_aeroporto is None:
        raise HTTPException(status_code=404, detail="Aeroporto não encontrado")
    
    for field, value in aeroporto.model_dump(exclude_unset=True).items():
        setattr(db_aeroporto, field, value)

    db.session.commit()
    db.session.refresh(db_aeroporto)

    return db_aeroporto


@app.post("/pagar-reserva/", response_model=PagamentoSchema)
async def pagar_reserva(pagamento: PagamentoSchema):

    reserva = db.session.query(Reserva).filter(Reserva.id == pagamento.reserva_id).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    db_pagamento = Pagamento(reserva_id=pagamento.reserva_id, valor=pagamento.valor, tipo=pagamento.tipo, status=pagamento.status)

    if db_pagamento.valor == reserva.voo.preco:
        print(reserva.voo.preco)
        reserva.status = "Pago"
        db.session.commit()

    db.session.add(db_pagamento)
    db.session.commit()
    return db_pagamento


@app.get("/voos/")
async def voos():
    voos = db.session.query(Voo).all()
    return voos


@app.post("/voos/create/", response_model=VooSchema)
async def create_voo(voo: VooSchema):
    db_voo = Voo(origem_id=voo.origem_id, destino_id=voo.destino_id, data_hora_partida=voo.data_hora_partida, capacidade=voo.capacidade, preco=voo.preco, numero_voo=voo.numero_voo)
    
    db.session.add(db_voo)
    db.session.commit()
    return db_voo


@app.put("/voos/edit/{voo_id}/", response_model=VooEditSchema)
async def edit_usuario(voo_id: int, voo: VooEditSchema):
    db_voo = db.session.query(Voo).filter(Voo.id == voo_id).first()
    if db_voo is None:
        raise HTTPException(status_code=404, detail="Voo não encontrado")
    
    for field, value in voo.model_dump(exclude_unset=True).items():
        setattr(db_voo, field, value)

    db.session.commit()
    db.session.refresh(db_voo)

    return db_voo


@app.get("/reservas/")
async def reservas():
    reservas = db.session.query(Reserva).all()
    return reservas


@app.post("/reservas/create/", response_model=ReservaSchema)
async def create_reserva(reserva: ReservaSchema):
    db_reserva = Reserva(usuario_id=reserva.usuario_id, voo_id=reserva.voo_id, data=reserva.data, status=reserva.status)
    db.session.add(db_reserva)
    db.session.commit()
    return db_reserva


@app.put("/reservas/edit/{reserva_id}/", response_model=ReservaEditSchema)
async def edit_usuario(reserva_id: int, reserva: ReservaEditSchema):
    db_reserva = db.session.query(Reserva).filter(Reserva.id == reserva_id).first()
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    for field, value in reserva.model_dump(exclude_unset=True).items():
        setattr(db_reserva, field, value)

    db.session.commit()
    db.session.refresh(db_reserva)

    return db_reserva
