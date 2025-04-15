from schemas.base import IDMixin, TableBase

from schemas.base import ReservationsBase


class TableCreate(TableBase):
    ...


class TableResponse(TableBase, IDMixin):
    ...


class TableReservationOut(ReservationsBase, IDMixin):
    ...


class TableOutWithReservations(TableBase, IDMixin):
    reservations: list[TableReservationOut] = []
