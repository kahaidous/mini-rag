from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, validator

class Project(BaseModel):
    _id: Optional[ObjectId]
    project_id: str = Field(..., min_length=1)

    @validator('project_id')
    def validate_project(cls, value):
        if not value.isalnum():
            return ValueError("project_id must be alphanumeric")
        
        return value
    
    class Config:
        arbitrary_type_allowed = True