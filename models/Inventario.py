from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Inventario(Base):
    __tablename__ = "inventario"

    id: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column()
    marca: Mapped[str] = mapped_column()
    modelo: Mapped[str] = mapped_column()
    serie: Mapped[str] = mapped_column()
    cantidad: Mapped[int] = mapped_column()
    asignado: Mapped[bool] = mapped_column()
    multi_serial: Mapped[bool] = mapped_column()
    almacenado: Mapped[bool] = mapped_column()
    en_carro: Mapped[bool] = mapped_column()
    estado: Mapped[str] = mapped_column()
    bodega: Mapped["Bodega"] = relationship(back_populates="inventario")
    movimientos: Mapped[List["Movimientos"]] = relationship(back_populates="inventario")
    carro: Mapped["MaterialMayor"] = relationship(back_populates="inventario")
    # multiseries: Mapped[List["Multiseries"]] = relationship(back_populates="inventario")


class Bodega(Base):
    __tablename__ = "bodega"

    id: Mapped[int] = mapped_column(primary_key=True)
    inventario_id: Mapped[int] = mapped_column(ForeignKey("inventario.id"))
    inventario: Mapped["Inventario"] = relationship(back_populates="bodega")
    cantidad: Mapped[int]
    fecha_ingreso: Mapped[datetime]


class Movimientos(Base):
    __tablename__ = "movimientos"

    id: Mapped[int] = mapped_column(primary_key=True)
    inventario_id: Mapped[int] = mapped_column(ForeignKey("inventario.id"))
    inventario: Mapped["Inventario"] = relationship(back_populates="movimientos")
    detalle: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()


class MaterialMayor(Base):
    __tablename__ = "Material_Mayor"

    id: Mapped[int] = mapped_column(primary_key=True)
    inventario_id: Mapped[int] = mapped_column(ForeignKey("inventario.id"))
    inventario: Mapped["Inventario"] = relationship(back_populates="carro")
    ubicacion: Mapped[str] = mapped_column()


class Asignados(Base):
    __tablename__ = "asignados"

    id: Mapped[int] = mapped_column(primary_key=True)
    inventario_id: Mapped[int] = mapped_column(ForeignKey("inventario.id"))
    inventario: Mapped["Inventario"] = relationship(back_populates="asignados")
    bombero_asignado: Mapped[str] = mapped_column()


# class Multiseries(Base):
#     __tablename__ = "multiseries"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     inventario_id: Mapped[int] = mapped_column(ForeignKey("inventario.id"))
#     inventario: Mapped["Inventario"] = relationship(back_populates="multiseries")
#     serie: Mapped[str] = mapped_column()
