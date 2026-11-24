from datetime import datetime, timezone

from sqlalchemy import(
    Boolean,
    Computed,
    DateTime,
    Enum as SAEnum,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums.user_role import UserRole
from app.infrastructure.database.base import Base

def utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

class User(Base):

    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint(
            "super_admin_slot",
            name="uq_users_single_super_admin"
        ),
        Index(
            "ix_users_role_active",
            "role",
            "is_active"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(254),
        nullable=False,
        unique=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        SAEnum(
            UserRole,
            values_callable=lambda cls: [
                role.value for role in cls
            ],
            native_enum=False,
            create_constraint=True,
            length=20,
            name="user_role",
        ),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    super_admin_slot: Mapped[int | None] = mapped_column(
        Integer,
        Computed(
            "CASE WHEN role = 'SUPER_ADMIN' THEN 1 ELSE NULL END",
            persisted=True
        ),
        nullable=True
    )

    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )