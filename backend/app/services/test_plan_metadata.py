from datetime import datetime


def build_test_plan_metadata():

    return {

        "generated_at": str(
            datetime.utcnow()
        ),

        "compiler_version": "0.12",

        "supports_self_healing": True,

        "supports_api_diffing": True
    }