from datetime import datetime
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashPassword: Mapped[str] = mapped_column(String(255), nullable=False)

    isActive: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    hashedResetToken: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    hashedResetTokenExpiry: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
