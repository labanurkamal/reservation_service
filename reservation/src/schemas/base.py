from datetime import datetime
from typing import Annotated

import pytz
from pydantic import BaseModel, Field

MAX_LENGTH: int = 100
NAME_LENGTH: int = 36
DEFAULT_DURATION: int = 60


def utc_now():
    return pytz.UTC.localize(datetime.now())


class IDMixin(BaseModel):
    id: int


class TableBase(BaseModel):
    name: Annotated[str, Field(default='Table 1', max_length=MAX_LENGTH)]
    seats: Annotated[int, Field(ge=1)]
    location: Annotated[str, Field(default='Терраса', max_length=MAX_LENGTH)]


class ReservationsBase(BaseModel):
    customer_name: Annotated[str, Field(..., max_length=NAME_LENGTH)]
    reservation_time: Annotated[datetime, Field(default_factory=utc_now)]
    duration_minutes: Annotated[int, Field(default=DEFAULT_DURATION, ge=1)]
