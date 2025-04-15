from datetime import datetime

from pydantic import BaseModel, Field


class TableCreateTest(BaseModel):
    name: str = Field('Table 1', max_length=100, description="Название столика")
    seats: int = Field(12, ge=1, description="Количество мест")
    location: str = Field('The window', max_length=100, description="Местоположение столика")


class TableResponseTest(BaseModel):
    id: int
    name: str
    seats: int
    location: str


class ReservationCreateTest(BaseModel):
    customer_name: str = Field('test_customer_name', max_length=36, description="Имя клиента")
    reservation_time: datetime = Field(..., description="Время бронирования")
    duration_minutes: int = Field(60, ge=1, description="Длительность бронирования в минутах")
    table_id: int = Field(..., ge=1, description="ID столика для бронирования")


class ReservationsResponseTest(BaseModel):
    id: int
    customer_name: str
    reservation_time: datetime
    duration_minutes: int
    table: TableResponseTest
