import json

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from fastapi.responses import FileResponse

from app.services.parser_router import parse_api_spec
from app.services.correlation_engine import detect_patterns
from app.services.prompt_engine import build_prompt
from app.services.llm_engine import LLMEngine
from app.services.jmx_builder import build_jmx
from app.services.xml_validator import validate_xml
from app.services.response_cleaner import (
    clean_llm_response
)

router = APIRouter()


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

        # Config object
        class Config:
            pass

        config = Config()

        config.users = users
        config.ramp_up = ramp_up
        config.duration = duration
        config.think_time = think_time

        # Build AI prompt
        prompt = build_prompt(
            parsed_apis,
            config,
            patterns
        )

        print("PROMPT GENERATED")

        # Generate AI response
        llm = LLMEngine()

        result = llm.generate(
            provider,
            prompt
        )

        print("RAW AI RESPONSE:")
        print(result)

        # Parse AI JSON response
        cleaned_result = clean_llm_response(
            result
        )

        print("CLEANED AI RESPONSE:")
        print(cleaned_result)

        test_plan = json.loads(
            cleaned_result
        )

        print("STRUCTURED TEST PLAN:")
        print(test_plan)

        # Build deterministic JMX
        jmx_content = build_jmx(
            test_plan
        )

        print("JMX GENERATED")

        # Validate generated XML
        print("GENERATED JMX:")
        print(jmx_content)

        validation = validate_xml(
            jmx_content
        )

        print("VALIDATION RESULT:")
        print(validation)

        if not validation["valid"]:

            return {
                "error": "Generated XML is invalid",
                "validation": validation
            }

        # Save JMX file
        output_path = "output/generated_test_plan.jmx"

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(jmx_content)

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