from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth, users, projects, collections, requests, ai

app = FastAPI(title=settings.APP_NAME, description="AI-assisted API testing and reliability platform", version="0.2.0")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(collections.router, prefix="/api/v1")
app.include_router(requests.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")

@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to API Sentinel", "version": "0.2.0"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "application": settings.APP_NAME}
