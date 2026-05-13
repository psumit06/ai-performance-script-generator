def detect_patterns(content):

    content = content.lower()

    return {
        "jwt": "jwt" in content or "token" in content,
        "auth": "authorization" in content,
        "session": "session" in content,
        "cookie": "cookie" in content
    }