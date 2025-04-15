from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Table(Base):
    """Модель столика в ресторане."""

    __table_args__ = (
        UniqueConstraint('name', 'location', name='uix_name_location'),
        {'comment': 'Cтолик в ресторане'}
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)

    reservations: Mapped[list["Reservation"]] = relationship(
        "Reservation",
        back_populates="table",
        cascade="all, delete-orphan",
        lazy="joined"
    )
