from datetime import date
from typing import (
    TYPE_CHECKING,
    List,
)
from uuid import UUID

from sqlalchemy import (
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.models import Base

if TYPE_CHECKING:
    from teams.models import Team


class RoleEnum(Enum):
    Empl: str = "Employee"
    Manager: str = "Manager"
    Admin: str = "Administrator"


class GenderEnum(Enum):
    male: str = "Man"
    female: str = "Woman"


class Users(Base):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped["GenderEnum"] = mapped_column(nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    role: Mapped["RoleEnum"] = mapped_column(nullable=True)
    departament_uuid: Mapped[UUID] = mapped_column(
        f"{ForeignKey(Structure.__tablename__)}.uuid",
        ondelete="SET NULL",
        nullable=False,
    )
    departament: Mapped["Structure"] = relationship(
        "Structure",
        back_populates="workers",
    )
    head_of: Mapped["StructureElement"] = relationship(
        "StructureElement",
        back_populates="director",
    )
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="author")
    tasks: Mapped[List["Tasks"]] = relationship("Tasks", back_populates="performer")
    team: Mapped["Team"] = relationship(
        "Team",
        back_populates="owner_id",
    )
