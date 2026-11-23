from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def create_project(db: Session, owner_id: UUID, data: ProjectCreate) -> Project:
    values = data.model_dump()
    values["base_url"] = str(values["base_url"])
    project = Project(owner_id=owner_id, **values)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_projects(db: Session, owner_id: UUID) -> list[Project]:
    return list(db.scalars(select(Project).where(Project.owner_id == owner_id).order_by(Project.created_at.desc())).all())

def get_project(db: Session, owner_id: UUID, project_id: UUID) -> Project | None:
    return db.scalars(select(Project).where(Project.id == project_id, Project.owner_id == owner_id)).first()

def update_project(db: Session, project: Project, data: ProjectUpdate) -> Project:
    values = data.model_dump(exclude_unset=True)
    if values.get("base_url") is not None:
        values["base_url"] = str(values["base_url"])
    for key, value in values.items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
