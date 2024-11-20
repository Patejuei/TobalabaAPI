from fastapi import APIRouter
from models.Tables import Ingresos, Egresos, Saldo as SaldoModel, Cuotas
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import engine
from pydantic import BaseModel
from datetime import datetime

cash = APIRouter()


class Cuota(BaseModel):
    personal_id: int


class Ingreso(BaseModel):
    fecha: datetime
    concepto: str
    valor: float
    tipo: str
    es_cuota: bool
    cuota: Cuota | None


class Egreso(BaseModel):
    fecha: datetime
    concepto: str
    valor: float
    tipo: str


class Saldo(BaseModel):
    fecha: datetime
    valor: float


@cash.get("/ingresos")
async def get_ingresos():
    with Session(engine) as session:
        stmt = select(Ingresos)
        ingresos = session.scalars(stmt).all()
        return ingresos


@cash.get("/egresos")
async def get_egresos():
    with Session(engine) as session:
        stmt = select(Egresos)
        egresos = session.scalars(stmt).all()
        return egresos


@cash.get("/saldo")
async def get_saldo():
    with Session(engine) as session:
        stmt = select(SaldoModel)
        saldo = session.scalars(stmt).all()
        return saldo


@cash.get("/cuotas/{personal_id}")
async def get_cuotas(personal_id: int):
    with Session(engine) as session:
        stmt = (
            select(Cuotas).join(Cuotas.ingreso).where(Cuotas.personal_id == personal_id)
        )
        cuotas = session.scalars(stmt).all()
        return cuotas


@cash.get("/cuotas")
async def get_all_cuotas():
    with Session(engine) as session:
        stmt = select(Cuotas).join(Cuotas.ingreso)
        cuotas = session.scalars(stmt).all()
        return cuotas


@cash.post("/ingresos", response_model=Ingreso)
async def create_ingreso(ingreso: Ingreso) -> Ingreso:
    with Session(engine) as session:
        new_ingreso = Ingresos(
            fecha=ingreso.fecha,
            concepto=ingreso.concepto,
            valor=ingreso.valor,
            tipo=ingreso.tipo,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        old_saldo = session.scalars(
            select(SaldoModel).order_by(SaldoModel.created_at.desc())
        ).first()
        new_saldo = SaldoModel(
            fecha=ingreso.fecha,
            valor=old_saldo.valor + ingreso.valor,
            es_ingerso=True,
            ingreso=new_ingreso,
            created_at=datetime.now(),
        )
        session.add_all([new_ingreso, new_saldo])
        if ingreso.es_cuota:
            new_cuota = Cuotas(
                ingreso=new_ingreso,
                personal_id=ingreso.cuota.personal_id,
            )
            session.add(new_cuota)
        session.commit()
        session.refresh(new_ingreso)
        return new_ingreso


@cash.post("/egresos", response_model=Egreso)
async def create_egreso(egreso: Egreso) -> Egreso:
    with Session(engine) as session:
        new_egreso = Egresos(
            fecha=egreso.fecha,
            concepto=egreso.concepto,
            valor=egreso.valor,
            tipo=egreso.tipo,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        old_saldo = session.scalars(
            select(SaldoModel).order_by(SaldoModel.created_at.desc())
        ).first()
        new_saldo = SaldoModel(
            fecha=egreso.fecha,
            valor=old_saldo.valor - egreso.valor,
            es_ingerso=False,
            egreso=new_egreso,
            created_at=datetime.now(),
        )
        session.add_all([new_egreso, new_saldo])
        session.commit()
        session.refresh(new_egreso)
        return new_egreso
