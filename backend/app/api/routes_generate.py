from fastapi import APIRouter

from app.models.request_models import GenerateRequest

from app.services.parser import parse_postman_collection
from app.services.correlation_engine import detect_patterns
from app.services.prompt_engine import build_prompt
from app.services.llm_engine import LLMEngine

router = APIRouter()


@router.post("/generate")
def generate(req: GenerateRequest):

    try:

        # STEP 1 — Parse incoming Postman collection
        parsed_apis = parse_postman_collection(
            req.api_spec
        )

        print("PARSED APIS:")
        print(parsed_apis)

        # STEP 2 — Detect patterns for correlation
        patterns = detect_patterns(
            parsed_apis
        )

        print("DETECTED PATTERNS:")
        print(patterns)

        # STEP 3 — Build structured AI prompt
        prompt = build_prompt(
            parsed_apis=parsed_apis,
            config=req.config,
            patterns=patterns
        )

        print("PROMPT GENERATED")

        # STEP 4 — Generate AI response
        llm = LLMEngine()

        result = llm.generate(
            provider=req.provider,
            prompt=prompt
        )

        print("AI RESPONSE RECEIVED")

        # STEP 5 — Return response
        return {
            "response": result
        }

    except Exception as e:

        print("ERROR:")
        print(str(e))

        return {
            "error": str(e)
        }