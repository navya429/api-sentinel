from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories import user_repository
from app.schemas.user import UserCreate

def register_user(db: Session, data: UserCreate):
    if user_repository.get_user_by_email(db, str(data.email)):
        return None
    try:
        return user_repository.create_user(db, str(data.email), hash_password(data.password))
    except Exception:
        # A concurrent registration may win the unique-email race.
        db.rollback()
        if user_repository.get_user_by_email(db, str(data.email)):
            return None
        raise

def authenticate_user(db: Session, email: str, password: str) -> str | None:
    user = user_repository.get_user_by_email(db, email)
    if user is None or not user.is_active or not verify_password(password, user.hashed_password):
        return None
    return create_access_token(str(user.id))
