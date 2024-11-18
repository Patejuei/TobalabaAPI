from fastapi import APIRouter
from models.Tables import (
    Inventario,
    Bodega as BodegaModel,
    Movimientos,
    MaterialMayor as MMayorModel,
    Asignados,
    BitacoraTemplate,
    ChecklistTemplate,
)
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import engine
from pydantic import BaseModel
from datetime import datetime


items = APIRouter()


class Bodega(BaseModel):
    cantidad: int
    fecha_ingreso: datetime


class MaterialMayor(BaseModel):
    carro: str
    ubicacion: str


class Bitacora(BaseModel):
    campo: str


class CheckList(BaseModel):
    campo: str


class Item(BaseModel):
    descripcion: str
    marca: str
    modelo: str
    serie: str
    cantidad: int
    asignado: bool
    multi_serial: bool
    has_checklist: bool
    has_bitacora: bool
    almacenado: bool
    en_carro: bool
    estado: str
    bodega: Bodega | None
    carro: MaterialMayor | None
    asignado_a: int | None
    movimiento: str
    bitacora: List[Bitacora] | None
    checklist: List[CheckList] | None


@items.get("/items")
async def get_items():
    with Session(engine) as session:
        stmt = select(Inventario)
        inventario = session.scalars(stmt).all()
        return inventario


@items.post("/items", response_model=Item)
async def create_item(item: Item) -> Item:
    """
    Agrega un nuevo item al inventario.

    Args:
      item: Item, objeto que se va a agregar al inventario.

    Returns:
      Item, el item que se acaba de agregar.
    """
    checklists = []
    bitacoras = []
    inventario = Inventario(
        descripcion=item.descripcion,
        marca=item.marca,
        modelo=item.modelo,
        serie=item.serie,
        cantidad=item.cantidad,
        checklist=item.checklist,
        bitacora=item.bitacora,
        es_asignado=item.asignado,
        multi_serial=item.multi_serial,
        almacenado=item.almacenado,
        en_carro=item.en_carro,
        estado=item.estado,
    )
    if item.almacenado:
        bodega = BodegaModel(
            inventario=inventario,
            cantidad=item.bodega.cantidad,
            fecha_ingreso=item.bodega.fecha_ingreso,
        )
    elif item.en_carro:
        carro = MMayorModel(
            inventario=inventario,
            carro=item.carro.carro,
            ubicacion=item.carro.ubicacion,
        )
    elif item.asignado:
        asignado = Asignados(
            inventario=inventario,
            personal_id=item.asignado_a,
        )

    if item.has_checklist:
        for i in item.checklist:
            checklists.append(
                ChecklistTemplate(
                    inventario=inventario,
                    campo=i.campo,
                )
            )
    if item.has_bitacora:
        for i in item.bitacora:
            bitacoras.append(
                BitacoraTemplate(
                    inventario=inventario,
                    campo=i.campo,
                )
            )
    movimiento = Movimientos(
        inventario=inventario,
        detalle=item.movimiento,
        created_at=datetime.now(),
    )
    with Session(engine) as session:
        session.add_all([inventario, movimiento])
        session.add_all(checklists) if item.has_checklist else None
        session.add_all(bitacoras) if item.has_bitacora else None
        session.add(bodega) if item.almacenado else None
        session.add(carro) if item.en_carro else None
        session.add(asignado) if item.asignado else None
        session.commit()
        return item


@items.get("/items/{item_id}", response_model=None)
async def get_item(item_id: int) -> Inventario:
    response = []
    with Session(engine) as session:
        stmt = select(Inventario).where(Inventario.id == item_id)
        item = session.scalars(stmt).first()
        response.append(item)
        if item.almacenado:
            stmt = select(BodegaModel).where(BodegaModel.inventario_id == item_id)
            bodega = session.scalars(stmt).first()
            response.append(bodega)
        elif item.en_carro:
            stmt = select(MMayorModel).where(MMayorModel.inventario_id == item_id)
            carro = session.scalars(stmt).first()
            response.append(carro)
        elif item.asignado:
            stmt = select(Asignados).where(Asignados.inventario_id == item_id)
            asignado = session.scalars(stmt).first()
            response.append(asignado)

        stmt = select(Movimientos).where(Movimientos.inventario_id == item_id)
        movimientos = session.scalars(stmt).all()
        response.append(movimientos)

        return response


@items.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item) -> Item:
    with Session(engine) as session:
        stmt = select(Inventario).where(Inventario.id == item_id)
        db_item = session.scalars(stmt).first()
        db_item.descripcion = item.descripcion
        db_item.marca = item.marca
        db_item.modelo = item.modelo
        db_item.serie = item.serie
        db_item.cantidad = item.cantidad
        db_item.es_asignado = item.asignado
        db_item.checklist = item.checklist
        db_item.bitacora = item.bitacora
        db_item.multi_serial = item.multi_serial
        db_item.almacenado = item.almacenado
        db_item.en_carro = item.en_carro
        db_item.estado = item.estado
        if db_item.almacenado:
            rel_stmt = select(BodegaModel).where(BodegaModel.inventario_id == item_id)
        elif db_item.en_carro:
            rel_stmt = select(MMayorModel).where(MMayorModel.inventario_id == item_id)
        elif db_item.asignado:
            rel_stmt = select(Asignados).where(Asignados.inventario_id == item_id)
        session.delete(rel_stmt)
        if item.almacenado:
            bodega = BodegaModel(
                inventario=db_item,
                cantidad=item.bodega.cantidad,
                fecha_ingreso=item.bodega.fecha_ingreso,
            )
            session.add(bodega)
        elif item.en_carro:
            carro = MMayorModel(
                inventario=db_item,
                carro=item.carro.carro,
                ubicacion=item.carro.ubicacion,
            )
            session.add(carro)
        elif item.asignado:
            asignado = Asignados(
                inventario=db_item,
                personal_id=item.asignado_a,
            )
            session.add(asignado)
        movimiento = Movimientos(
            inventario=db_item,
            detalle=item.movimiento,
            created_at=datetime.now(),
        )
        session.add(movimiento)
        session.commit()
        session.refresh(db_item)

        return db_item
