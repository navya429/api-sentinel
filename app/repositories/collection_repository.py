from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Collection

def create_collection(db: Session, project_id: UUID, name: str, description: str | None) -> Collection:
    item = Collection(project_id=project_id, name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_collections(db: Session, project_id: UUID) -> list[Collection]:
    return list(db.scalars(select(Collection).where(Collection.project_id == project_id).order_by(Collection.created_at.desc())).all())

def get_collection(db: Session, collection_id: UUID) -> Collection | None:
    return db.get(Collection, collection_id)
