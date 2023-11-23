from __future__ import annotations

import uuid
from typing import List
from typing import TYPE_CHECKING

from db.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from db.passwords.models import Password


class User(Base):
    user_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4(), server_default=str(uuid.uuid4())
    )
    login: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))

    passwords: Mapped[List[Password]] = relationship(back_populates="user")
