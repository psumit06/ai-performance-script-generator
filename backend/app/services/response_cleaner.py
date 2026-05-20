import re


def clean_llm_response(response):

    if not response:
        return ""

    response = response.strip()

    # Remove markdown fences
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

    return response.strip()