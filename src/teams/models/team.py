from typing import (
    TYPE_CHECKING,
    List,
)
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.models import Base

if TYPE_CHECKING:
    from users.models import User
    from tasks.models import Task


class Team(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    owner_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid"),
        nullable=False,
    )
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="owned_teams",
    )
    members: Mapped[List["User"]] = relationship(
        "User",
        foreign_keys="User.team_uuid",
        back_populates="team",
    )
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="team",
    )
