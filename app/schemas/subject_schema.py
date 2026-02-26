from pydantic import BaseModel


class SubjectBase(BaseModel):
    subject_name: str


class SubjectResponse(SubjectBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True
