from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.models import Base

if TYPE_CHECKING:
    from users.models import Users

class Team(Base):
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    owner_id: Mapped["Users"] = relationship(
        "Users",
        back_populates="team"
    )
