import re


def clean_llm_response(response):

    if not response:

        return ""

    response = response.strip()

    # REMOVE MARKDOWN
    response = re.sub(
        r"```json",
        "",
        response
    )

    response = re.sub(
        r"```",
        "",
        response
    )

    # REMOVE LEADING EXPLANATIONS
    response = response.strip()

    # FIND FIRST JSON OBJECT
    start = response.find("{")

    end = response.rfind("}")

    if start != -1 and end != -1:

        response = response[
            start:end + 1
        ]

    return response.strip()