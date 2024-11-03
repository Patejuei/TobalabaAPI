from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Ingresos(Base):
    __tablename__ = "Tesoreria_Ingresos"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[datetime] = mapped_column()
    concepto: Mapped[str] = mapped_column()
    valor: Mapped[float] = mapped_column()
    tipo: Mapped[str] = mapped_column()
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
