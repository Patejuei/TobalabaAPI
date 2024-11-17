from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List
from datetime import datetime
from config.database import Base, engine


class Inventario(Base):
    __tablename__ = "inventario"

    id: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column()
    marca: Mapped[str] = mapped_column()
    modelo: Mapped[str] = mapped_column()
    serie: Mapped[str] = mapped_column()
    cantidad: Mapped[int] = mapped_column()
    es_asignado: Mapped[bool] = mapped_column()
    multi_serial: Mapped[bool] = mapped_column()
    almacenado: Mapped[bool] = mapped_column()
    en_carro: Mapped[bool] = mapped_column()
    estado: Mapped[str] = mapped_column()
    bodega: Mapped["Bodega"] = relationship(back_populates="inventario")
    movimientos: Mapped[List["Movimientos"]] = relationship(back_populates="inventario")
    carro: Mapped["MaterialMayor"] = relationship(back_populates="inventario")
    asignado: Mapped["Asignados"] = relationship(back_populates="inventario")
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
    inventario: Mapped["Inventario"] = relationship(back_populates="asignado")
    personal_id: Mapped[int] = mapped_column(ForeignKey("personal.id"))
    personal: Mapped["PersonalModel"] = relationship(back_populates="item_asignado")


# class Multiseries(Base):
#     __tablename__ = "multiseries"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     inventario_id: Mapped[int] = mapped_column(ForeignKey("inventario.id"))
#     inventario: Mapped["Inventario"] = relationship(back_populates="multiseries")
#     serie: Mapped[str] = mapped_column()


class PersonalModel(Base):
    __tablename__ = "personal"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column()
    apellido_paterno: Mapped[str] = mapped_column()
    apellido_materno: Mapped[str] = mapped_column()
    rut: Mapped[int] = mapped_column()
    dv: Mapped[str] = mapped_column()
    fecha_nacimiento: Mapped[datetime] = mapped_column()
    fecha_ingreso: Mapped[datetime] = mapped_column()
    telefono: Mapped[int] = mapped_column()
    correo: Mapped[str] = mapped_column()
    estado: Mapped[str] = mapped_column()
    cargo: Mapped[str] = mapped_column()
    registro: Mapped[str] = mapped_column()
    item_asignado: Mapped[List["Asignados"]] = relationship(back_populates="personal")
    cuotas: Mapped[List["Cuotas"]] = relationship(back_populates="personal")


class Ingresos(Base):
    __tablename__ = "Tesoreria_Ingresos"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[datetime] = mapped_column()
    concepto: Mapped[str] = mapped_column()
    valor: Mapped[float] = mapped_column()
    tipo: Mapped[str] = mapped_column()
    cuotas: Mapped["Cuotas"] = relationship(back_populates="ingreso")
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()


class Egresos(Base):
    __tablename__ = "Tesoreria_Egresos"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[datetime] = mapped_column()
    concepto: Mapped[str] = mapped_column()
    valor: Mapped[float] = mapped_column()
    tipo: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()


class Saldo(Base):
    __tablename__ = "Tesoreria_Saldo"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[datetime] = mapped_column()
    valor: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()


class Cuotas(Base):
    __tablename__ = "Tesoreria_Cuotas"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[datetime] = mapped_column()
    ingreso: Mapped["Ingresos"] = relationship(back_populates="cuotas")
    ingreso_id: Mapped[int] = mapped_column(ForeignKey("Tesoreria_Ingresos.id"))
    personal: Mapped["PersonalModel"] = relationship(back_populates="cuotas")
    personal_id: Mapped[int] = mapped_column(ForeignKey("personal.id"))


def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)
