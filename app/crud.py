from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Student
from app.schemas import StudentCreate, StudentUpdate


def get_students(
    db: Session,
    search: str | None = None,
    course: str | None = None,
    status: str | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[Student]:
    statement = select(Student)

    if search:
        term = f"%{search.strip()}%"
        statement = statement.where(
            Student.name.ilike(term)
            | Student.email.ilike(term)
        )

    if course:
        statement = statement.where(Student.course == course)

    if status:
        statement = statement.where(Student.status == status)

    statement = (
        statement.order_by(Student.id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def get_student(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def create_student(db: Session, data: StudentCreate) -> Student:
    student = Student(**data.model_dump(by_alias=False))

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def update_student(
    db: Session,
    student: Student,
    data: StudentUpdate,
) -> Student:
    changes = data.model_dump(
        exclude_unset=True,
        by_alias=False,
    )

    
    required_fields = {"name", "email", "course", "grade", "status"}
    for field in required_fields:
        if field in changes and changes[field] is None:
            raise ValueError(f"{field} cannot be null")

    for field, value in changes.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student: Student) -> None:
    db.delete(student)
    db.commit()


def get_student_stats(db: Session) -> dict[str, int]:
    total = db.scalar(select(func.count()).select_from(Student)) or 0

    active = (
        db.scalar(
            select(func.count())
            .select_from(Student)
            .where(Student.status == "Active")
        )
        or 0
    )

    inactive = (
        db.scalar(
            select(func.count())
            .select_from(Student)
            .where(Student.status == "Inactive")
        )
        or 0
    )

    return {
        "total": total,
        "active": active,
        "inactive": inactive,
    }
