from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import APIRequest

def create_request(db: Session, collection_id: UUID, values: dict) -> APIRequest:
    item = APIRequest(collection_id=collection_id, **values)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_requests(db: Session, collection_id: UUID) -> list[APIRequest]:
    return list(db.scalars(select(APIRequest).where(APIRequest.collection_id == collection_id).order_by(APIRequest.created_at.desc())).all())

def get_request(db: Session, request_id: UUID) -> APIRequest | None:
    return db.get(APIRequest, request_id)
