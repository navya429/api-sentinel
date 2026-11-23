from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.common import ORMModel

class CollectionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)

class CollectionResponse(ORMModel):
    id: UUID
    project_id: UUID
    name: str
    description: str | None
    created_at: datetime
