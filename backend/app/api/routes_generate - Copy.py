from unittest import result

from fastapi import APIRouter

from app.models.request_models import GenerateRequest
from app.services.xml_validator import validate_xml
from app.services.parser_router import parse_api_spec
from app.services.correlation_engine import detect_patterns
from app.services.prompt_engine import build_prompt
from app.services.llm_engine import LLMEngine
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.xml_cleaner import clean_ai_xml

router = APIRouter()


@router.post("/generate")
def generate(req: GenerateRequest):

    try:

        # STEP 1 — Parse incoming API specification
        parsed_apis = parse_api_spec(
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
        cleaned_result = clean_ai_xml(result)
        validation = validate_xml(cleaned_result)
        #print("XML VALIDATION RESULT:", validation)

        return {
            "response": cleaned_result,
            "validation": validation
        }

    except Exception as e:

        print("ERROR:")
        print(str(e))

        return {
            "error": str(e)
        }

@router.post("/generate-from-file")
async def generate_from_file(

    provider: str,
    users: int,
    ramp_up: int,
    duration: int,
    think_time: int,
    file: UploadFile = File(...)

):

    try:

        # Read uploaded file
        raw_content = await file.read()

        raw_content = raw_content.decode("utf-8")

        print("FILE RECEIVED")

        # Parse APIs
        parsed_apis = parse_api_spec(
            raw_content
        )

        print("PARSED APIS:")
        print(parsed_apis)

        # Detect patterns
        patterns = detect_patterns(
            parsed_apis
        )

        print("PATTERNS:")
        print(patterns)

        # Create config object
        class Config:
            pass

        config = Config()

        config.users = users
        config.ramp_up = ramp_up
        config.duration = duration
        config.think_time = think_time

        # Build prompt
        prompt = build_prompt(
            parsed_apis,
            config,
            patterns
        )

        # Generate AI response
        llm = LLMEngine()

        result = llm.generate(
            provider,
            prompt
        )

        print("RAW AI RESPONSE:")
        print(result)

        # Validate XML
        cleaned_result = clean_ai_xml(result)
        validation = validate_xml(cleaned_result)

        if not validation["valid"]:

            return {
                "error": "Generated XML is invalid",
                "validation": validation
            }

        # Save JMX file
        output_path = "output/generated_test_plan.jmx"

        with open(output_path, "w", encoding="utf-8") as f:

            f.write(cleaned_result)

        print("JMX FILE SAVED")

        # Return downloadable file
        return FileResponse(
            path=output_path,
            filename="generated_test_plan.jmx",
            media_type="application/xml"
        )

    except Exception as e:

        print("ERROR:")
        print(str(e))

        return {
            "error": str(e)
        }