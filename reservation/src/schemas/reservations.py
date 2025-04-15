from datetime import datetime
from typing import Annotated

import pytz
from pydantic import Field, field_validator

from schemas.base import IDMixin, ReservationsBase
from schemas.tables import TableResponse


class ReservationsCreate(ReservationsBase):
    table_id: Annotated[int, Field(..., ge=1)]

    @field_validator('reservation_time')
    @classmethod
    def validate_reservation_time(cls, v: datetime) -> datetime:
        v = v.replace(second=0, microsecond=0)
        now = datetime.now(tz=pytz.UTC).replace(second=0, microsecond=0)

        if v.tzinfo is None:
            v = pytz.UTC.localize(v)

        if v < now:
            raise ValueError("Время бронирования не может быть в прошлом.")

        return v


class ReservationsResponse(ReservationsBase, IDMixin):
    table: TableResponse
