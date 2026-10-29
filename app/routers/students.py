from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import (
    StudentCreate,
    StudentResponse,
    StudentStats,
    StudentStatus,
    StudentUpdate,
)


router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"],
)


@router.get("/stats", response_model=StudentStats)
def student_stats(db: Session = Depends(get_db)):
    return crud.get_student_stats(db)


@router.get("/", response_model=list[StudentResponse])
def list_students(
    search: str | None = None,
    course: Literal["React", "TypeScript", "Python", "Java"] | None = None,
    status_filter: StudentStatus | None = Query(default=None, alias="status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_students(
        db,
        search=search,
        course=course,
        status=status_filter,
        skip=skip,
        limit=limit,
    )


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return student


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create_student(db, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists",
        ) from exc


@router.patch("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db),
):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    try:
        return crud.update_student(db, student, data)
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists",
        ) from exc


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    crud.delete_student(db, student)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
