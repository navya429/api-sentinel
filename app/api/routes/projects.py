from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.repositories import project_repository
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(data: ProjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return project_repository.create_project(db, user.id, data)

@router.get("", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return project_repository.get_projects(db, user.id)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = project_repository.get_project(db, user.id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: UUID, data: ProjectUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = project_repository.get_project(db, user.id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_repository.update_project(db, project, data)

@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = project_repository.get_project(db, user.id, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    project_repository.delete_project(db, project)
    return Response(status_code=204)
