from fastapi import APIRouter
from models.Tables import PersonalModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import engine
from pydantic import BaseModel
from datetime import datetime


personal = APIRouter()


class Personal(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    rut: int
    dv: str
    fecha_nacimiento: datetime
    fecha_ingreso: datetime
    telefono: int
    correo: str
    estado: str
    cargo: str
    registro: str


@personal.get("/personal")
async def get_personal():
    with Session(engine) as session:
        stmt = select(PersonalModel)
        personal = session.scalars(stmt).all()
        return personal


@personal.post("/personal", response_model=Personal)
async def create_personal(personal: Personal) -> Personal:
    with Session(engine) as session:
        new_personal = PersonalModel(
            nombre=personal.nombre,
            apellido_paterno=personal.apellido_paterno,
            apellido_materno=personal.apellido_materno,
            rut=personal.rut,
            dv=personal.dv,
            fecha_nacimiento=personal.fecha_nacimiento,
            fecha_ingreso=personal.fecha_ingreso,
            telefono=personal.telefono,
            correo=personal.correo,
            estado=personal.estado,
            cargo=personal.cargo,
            registro=personal.registro,
        )
        session.add(new_personal)
        session.commit()
        session.refresh(new_personal)
        return new_personal


@personal.get("/personal/{personal_id}", response_model=Personal)
async def get_personal(personal_id: int) -> Personal:
    with Session(engine) as session:
        stmt = select(PersonalModel).where(PersonalModel.id == personal_id)
        personal = session.scalars(stmt).first()
        return personal


@personal.put("/personal/{personal_id}", response_model=Personal)
async def update_personal(personal_id: int, personal: Personal) -> Personal:
    with Session(engine) as session:
        stmt = select(PersonalModel).where(PersonalModel.id == personal_id)
        db_personal = session.scalars(stmt).first()
        db_personal.nombre = personal.nombre
        db_personal.apellido_paterno = personal.apellido_paterno
        db_personal.apellido_materno = personal.apellido_materno
        db_personal.rut = personal.rut
        db_personal.dv = personal.dv
        db_personal.fecha_nacimiento = personal.fecha_nacimiento
        db_personal.fecha_ingreso = personal.fecha_ingreso
        db_personal.telefono = personal.telefono
        db_personal.correo = personal.correo
        db_personal.estado = personal.estado
        db_personal.cargo = personal.cargo
        db_personal.registro = personal.registro
        session.commit()
        session.refresh(db_personal)
        return db_personal
