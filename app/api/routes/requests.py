from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.repositories import project_repository, collection_repository, request_repository
from app.schemas.api_request import APIRequestCreate, APIRequestResponse, ExecutionResponse
from app.services.execution_service import execute_saved_request

router = APIRouter(tags=["API Requests"])

def _owned_collection(db: Session, user: User, collection_id: UUID):
    collection = collection_repository.get_collection(db, collection_id)
    if collection is None or project_repository.get_project(db, user.id, collection.project_id) is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

@router.post("/collections/{collection_id}/requests", response_model=APIRequestResponse, status_code=201)
def create_request(collection_id: UUID, data: APIRequestCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _owned_collection(db, user, collection_id)
    return request_repository.create_request(db, collection_id, data.model_dump())

@router.get("/collections/{collection_id}/requests", response_model=list[APIRequestResponse])
def list_requests(collection_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _owned_collection(db, user, collection_id)
    return request_repository.list_requests(db, collection_id)

@router.post("/requests/{request_id}/run", response_model=ExecutionResponse)
def run_request(request_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = request_repository.get_request(db, request_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Request not found")
    _owned_collection(db, user, item.collection_id)
    return execute_saved_request(item)
