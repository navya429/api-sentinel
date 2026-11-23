from pydantic import BaseModel, Field

class GenerateTestsInput(BaseModel):
    endpoint_description: str = Field(min_length=10, max_length=4000)

class GeneratedTest(BaseModel):
    name: str
    method: str
    path: str
    expected_status: int
    purpose: str

class GenerateTestsResponse(BaseModel):
    provider: str
    tests: list[GeneratedTest]
