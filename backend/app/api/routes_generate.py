import json

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from fastapi.responses import FileResponse

from app.services.parser_router import parse_api_spec

from app.services.correlation_engine import (
    detect_patterns
)

from app.services.prompt_engine import (
    build_prompt
)

from app.services.llm_engine import (
    LLMEngine
)

from app.services.jmx_builder import (
    build_jmx
)

from app.services.xml_validator import (
    validate_xml
)

from app.services.response_cleaner import (
    clean_llm_response
)

# DAY 12 IMPORTS
from app.services.api_diff_engine import (
    compare_apis
)

from app.services.test_plan_metadata import (
    build_test_plan_metadata
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

        # =========================
        # READ UPLOADED FILE
        # =========================

        raw_content = await file.read()

        raw_content = raw_content.decode(
            "utf-8"
        )

        print("\n====================")
        print("FILE RECEIVED")
        print("====================\n")

        # =========================
        # PARSE APIs
        # =========================

        parsed_apis = parse_api_spec(
            raw_content
        )

        print("\n====================")
        print("PARSED APIS")
        print("====================\n")

        print(
            json.dumps(
                parsed_apis,
                indent=2
            )
        )

        # =========================
        # DETECT PATTERNS
        # =========================

        patterns = detect_patterns(
            parsed_apis
        )

        print("\n====================")
        print("PATTERNS")
        print("====================\n")

        print(
            json.dumps(
                patterns,
                indent=2
            )
        )

        # =========================
        # DAY 12 METADATA
        # =========================

        metadata = build_test_plan_metadata()

        print("\n====================")
        print("TEST PLAN METADATA")
        print("====================\n")

        print(
            json.dumps(
                metadata,
                indent=2
            )
        )

        # =========================
        # CONFIG OBJECT
        # =========================

        class Config:
            pass

        config = Config()

        config.users = users
        config.ramp_up = ramp_up
        config.duration = duration
        config.think_time = think_time

        # =========================
        # BUILD AI PROMPT
        # =========================

        prompt = build_prompt(
            parsed_apis,
            config,
            patterns
        )

        print("\n====================")
        print("PROMPT GENERATED")
        print("====================\n")

        # =========================
        # GENERATE AI RESPONSE
        # =========================

        llm = LLMEngine()

        result = llm.generate(
            provider,
            prompt
        )

        print("\n====================")
        print("RAW AI RESPONSE")
        print("====================\n")

        print(result)

        # =========================
        # CLEAN AI RESPONSE
        # =========================

        cleaned_result = clean_llm_response(
            result
        )

        print("\n====================")
        print("CLEANED AI RESPONSE")
        print("====================\n")

        print(cleaned_result)

        # =========================
        # PARSE STRUCTURED TEST PLAN
        # =========================

        test_plan = json.loads(
            cleaned_result
        )

        print("\n====================")
        print("STRUCTURED TEST PLAN")
        print("====================\n")

        print(
            json.dumps(
                test_plan,
                indent=2
            )
        )

        # =========================
        # DAY 12 FOUNDATION:
        # API DIFF ENGINE
        # =========================

        previous_apis = None

        if previous_apis:

            changes = compare_apis(
                previous_apis,
                parsed_apis
            )

            print("\n====================")
            print("API DIFF CHANGES")
            print("====================\n")

            print(
                json.dumps(
                    changes,
                    indent=2
                )
            )

        # =========================
        # BUILD DETERMINISTIC JMX
        # =========================

        jmx_content = build_jmx(
            test_plan
        )

        print("\n====================")
        print("JMX GENERATED")
        print("====================\n")

        # =========================
        # VALIDATE GENERATED XML
        # =========================

        print("\n====================")
        print("GENERATED JMX")
        print("====================\n")

        print(jmx_content)

        validation = validate_xml(
            jmx_content
        )

        print("\n====================")
        print("VALIDATION RESULT")
        print("====================\n")

        print(validation)

        if not validation["valid"]:

            return {
                "error": "Generated XML is invalid",
                "validation": validation
            }

        # =========================
        # SAVE JMX FILE
        # =========================

        output_path = (
            "output/generated_test_plan.jmx"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(jmx_content)

        print("\n====================")
        print("JMX FILE SAVED")
        print("====================\n")

        # =========================
        # RETURN DOWNLOADABLE FILE
        # =========================

        return FileResponse(

            path=output_path,

            filename="generated_test_plan.jmx",

            media_type="application/xml"
        )

    except Exception as e:

        print("\n====================")
        print("ERROR")
        print("====================\n")

        print(str(e))

        return {
            "error": str(e)
        }