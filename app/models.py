from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    __table_args__ = (
        CheckConstraint(
            "grade >= 0 AND grade <= 100",
            name="check_student_grade",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    course: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    grade: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Active",
    )

    photo_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )
    