# SQLAlchemy ORM models

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Date, ForeignKey, UniqueConstraint, ForeignKeyConstraint
from BackendService.db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)


class Race(Base):
    __tablename__ = "races"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(Date, nullable=False)


class UserRace(Base):
    __tablename__ = "user_race"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    race_id: Mapped[int] = mapped_column(ForeignKey("races.id", ondelete="CASCADE"), primary_key=True)
    bib_number: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint("race_id", "bib_number", name="uq_race_bib_number"),
    )


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_path: Mapped[str] = mapped_column(Text, nullable=False)


class ImageBib(Base):
    __tablename__ = "image_bibs"

    image_id: Mapped[int] = mapped_column(ForeignKey("images.id", ondelete="CASCADE"), primary_key=True)
    race_id: Mapped[int] = mapped_column(primary_key=True)
    bib_number: Mapped[int] = mapped_column(primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["race_id", "bib_number"],
            ["user_race.race_id", "user_race.bib_number"],
            ondelete="CASCADE"
        ),
    )
