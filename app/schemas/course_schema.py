from pydantic import BaseModel
from typing import List


class SubjectSimple(BaseModel):
    id: int
    subject_name: str

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    name: str


class CourseResponse(CourseBase):
    id: int
    subjects: List[SubjectSimple] = []

    class Config:
        from_attributes = True
