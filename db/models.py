from __future__ import annotations

from django.conf import settings
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    # Tests may create Movie without duration -> must not crash on NOT NULL
    duration = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name="movie_sessions")
    cinema_hall = models.ForeignKey(
        CinemaHall,
        on_delete=models.CASCADE,
        related_name="movie_sessions",
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {self.show_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="orders")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.created_at}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket_place_for_session",
            )
        ]

    def __str__(self) -> str:
        return f"{self.movie_session} (row: {self.row}, seat: {self.seat})"
