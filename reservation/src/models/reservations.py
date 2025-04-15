from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Reservation(Base):
    """Модель бронирования столика в ресторане."""

    __table_args__ = {'comment': 'Бронь'}

    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    reservation_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id", ondelete="CASCADE"), nullable=False)
    table: Mapped["Table"] = relationship(
        "Table",
        back_populates="reservations",
        lazy="joined"
    )
