from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models import User
from app.schemas.ai import GenerateTestsInput, GenerateTestsResponse
from app.services.ai_provider import provider

router = APIRouter(prefix="/ai", tags=["AI assistance"])

@router.post("/generate-tests", response_model=GenerateTestsResponse)
def generate_tests(data: GenerateTestsInput, user: User = Depends(get_current_user)):
    return {"provider": provider.name, "tests": provider.generate(data.endpoint_description)}
