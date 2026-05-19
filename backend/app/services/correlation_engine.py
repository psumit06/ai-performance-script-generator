def detect_patterns(parsed_apis):

    combined_text = ""

    # Loop through endpoints
    for ep in parsed_apis["endpoints"]:

        combined_text += str(ep.get("method", " "))
        combined_text += str(ep.get("url", " "))

        # Headers
        headers = ep.get("headers", [])

        for header in headers:

            combined_text += str(
                header.get("key", "")
            )

            combined_text += str(
                header.get("value", "")
            )

        # Body
        combined_text += str(
            ep.get("body", {})
        )

    # Convert everything to lowercase
    combined_text = combined_text.lower()

    # Detect patterns
    return {
        "jwt": "jwt" in combined_text or "token" in combined_text,
        "auth": "authorization" in combined_text,
        "session": "session" in combined_text,
        "cookie": "cookie" in combined_text
    }