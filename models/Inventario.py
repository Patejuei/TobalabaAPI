from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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