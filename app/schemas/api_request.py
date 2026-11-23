from datetime import datetime
from uuid import UUID
from typing import Any
from pydantic import BaseModel, Field
from app.schemas.common import ORMModel

class APIRequestCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    method: str = Field(pattern="^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)$")
    url: str = Field(min_length=8, max_length=2000)
    headers: dict[str, str] = Field(default_factory=dict)
    params: dict[str, str] = Field(default_factory=dict)
    body: str | None = None

class APIRequestResponse(ORMModel):
    id: UUID
    collection_id: UUID
    name: str
    method: str
    url: str
    headers: dict[str, Any]
    params: dict[str, Any]
    body: str | None
    created_at: datetime

class ExecutionResponse(BaseModel):
    request_id: UUID
    status_code: int
    elapsed_ms: float
    response_headers: dict[str, str]
    response_body: str
