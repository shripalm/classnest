from pydantic import BaseModel


class CourseBase(BaseModel):
    name: str


class CourseResponse(CourseBase):
    id: int
    class_id: int

    class Config:
        from_attributes = True
