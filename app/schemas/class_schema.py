from pydantic import BaseModel
from typing import List


class CourseSimple(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ClassBase(BaseModel):
    name: str


class ClassResponse(ClassBase):
    id: int
    courses: List[CourseSimple] = []

    class Config:
        from_attributes = True
