from fastapi import APIRouter
from models.Inventario import (
    Inventario,
    Bodega as BodegaModel,
    Movimientos,
    MaterialMayor,
    Asignados,
)
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import engine
from pydantic import BaseModel
from datetime import datetime


items = APIRouter()


class Bodega(BaseModel):
    cantidad: int
    fecha_ingreso: datetime


class Item(BaseModel):
    descripcion: str
    marca: str
    modelo: str
    serie: str
    cantidad: int
    asignado: bool
    multi_serial: bool
    almacenado: bool
    en_carro: bool
    estado: str
    bodega: Bodega | None
    carro: str | None


@items.get("/items")
async def get_items():
    with Session(engine) as session:
        stmt = select(Inventario)
        inventario = session.scalars(stmt).all()
        return inventario


@items.post("/items")
async def create_item(item: Item) -> Item:
    """
    Agrega un nuevo item al inventario.

    Args:
      item: Item, objeto que se va a agregar al inventario.

    Returns:
      Item, el item que se acaba de agregar.
    """
    inventario = Inventario(
        descripcion=item.descripcion,
        marca=item.marca,
        modelo=item.modelo,
        serie=item.serie,
        cantidad=item.cantidad,
        asignado=item.asignado,
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
    movimiento = Movimientos(
        inventario=inventario,
        detalle="Objeto añadido a la base de datos",
        created_at=datetime.now(),
    )
    with Session(engine) as session:
        session.add_all([inventario, movimiento])
        session.add(bodega) if item.almacenado else None
        session.commit()
        return item


@items.get("/items/{item_id}")
async def get_item(item_id: int) -> Inventario:
    response = []
    with Session(engine) as session:
        stmt = select(Inventario).where(Inventario.id == item_id)
        item = session.scalars(stmt).first()
        response.append(item)
        if item.almacenado:
            stmt = select(Bodega).where(Bodega.inventario_id == item_id)
            bodega = session.scalars(stmt).first()
            response.append(bodega)
        elif item.en_carro:
            stmt = select(MaterialMayor).where(MaterialMayor.inventario_id == item_id)
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
