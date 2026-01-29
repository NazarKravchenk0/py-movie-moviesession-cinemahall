from django.db.models import QuerySet

from db.models import CinemaHall


def get_cinema_halls() -> QuerySet[CinemaHall]:
    return CinemaHall.objects.all()


def create_cinema_hall(
    hall_name: str,
    rows: int,
    seats_in_row: int,
) -> CinemaHall:
    return CinemaHall.objects.create(
        name=hall_name,
        rows=rows,
        seats_in_row=seats_in_row,
    )
