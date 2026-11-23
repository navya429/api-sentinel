from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.repositories import project_repository, collection_repository
from app.schemas.collection import CollectionCreate, CollectionResponse

router = APIRouter(tags=["Collections"])

@router.post("/projects/{project_id}/collections", response_model=CollectionResponse, status_code=201)
def create_collection(project_id: UUID, data: CollectionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = project_repository.get_project(db, user.id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return collection_repository.create_collection(db, project_id, data.name, data.description)

@router.get("/projects/{project_id}/collections", response_model=list[CollectionResponse])
def list_collections(project_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = project_repository.get_project(db, user.id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return collection_repository.list_collections(db, project_id)
