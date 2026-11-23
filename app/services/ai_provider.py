from typing import Protocol
from app.schemas.ai import GeneratedTest

class TestGenerationProvider(Protocol):
    @property
    def name(self) -> str: ...
    def generate(self, endpoint_description: str) -> list[GeneratedTest]: ...

class ExampleRulesProvider:
    """Deterministic local provider; replace with an LLM provider when configured."""
    name = "example-rules"

    def generate(self, endpoint_description: str) -> list[GeneratedTest]:
        return [
            GeneratedTest(name="Successful response", method="GET", path="/", expected_status=200,
                          purpose=f"Verify the described endpoint responds successfully: {endpoint_description[:160]}"),
            GeneratedTest(name="Not found handling", method="GET", path="/missing-resource", expected_status=404,
                          purpose="Verify unknown resources return a not-found response."),
            GeneratedTest(name="Invalid input handling", method="POST", path="/", expected_status=422,
                          purpose="Verify invalid request data is rejected."),
        ]

provider: TestGenerationProvider = ExampleRulesProvider()
