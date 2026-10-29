from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


Course = Literal["React", "TypeScript", "Python", "Java"]
StudentStatus = Literal["Active", "Inactive"]


class StudentFields(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    course: Course
    grade: int = Field(ge=0, le=100)
    status: StudentStatus = "Active"
    photo_url: str | None = Field(
        default=None,
        alias="photoUrl",
        max_length=1000,
    )

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class StudentCreate(StudentFields):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    course: Course | None = None
    grade: int | None = Field(default=None, ge=0, le=100)
    status: StudentStatus | None = None
    photo_url: str | None = Field(
        default=None,
        alias="photoUrl",
        max_length=1000,
    )

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class StudentResponse(StudentFields):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class StudentStats(BaseModel):
    total: int
    active: int
    inactive: int