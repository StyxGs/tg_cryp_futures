from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base import Base

association_table = Table(
    "association_table",
    Base.metadata,
    Column('user_id', ForeignKey('tg_user.id'), primary_key=True),
    Column('cryp_future_id', ForeignKey('cryp_future.id'), primary_key=True),
)


class TgUser(Base):
    __tablename__ = 'tg_user'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    tg_user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    tg_username: Mapped[str] = mapped_column(String(50), nullable=True)
    cryp_future: Mapped[list['CrypFuture']] = relationship(secondary=association_table)

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, tg_user_id={self.tg_user_id!r})'


class CrypFuture(Base):
    __tablename__ = 'cryp_future'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'CrypFuture(id={self.id!r}, title={self.title!r})'
