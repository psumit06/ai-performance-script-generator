from fastapi import APIRouter
from ..models.request_models import GenerateRequest
from ..services.prompt_engine import build_prompt
from ..services.llmengine import LLMEngine
from app.services.correlation_engine import detect_patterns

router = APIRouter()


@router.post("/generate")
def generate(req: GenerateRequest):

    patterns = detect_patterns(
        req.api_spec
    )

    prompt = build_prompt(
        req.api_spec,
        req.config,
        patterns
    )

    llm = LLMEngine()

    result = llm.generate(
        req.provider,
        prompt
    )

    return {
        "response": result
    }