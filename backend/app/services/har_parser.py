import json


def parse_har(raw_content):

    data = json.loads(raw_content)

    entries = data.get("log", {}).get("entries", [])

    endpoints = []

    for entry in entries:

        request = entry.get("request", {})

        endpoint = {
            "name": request.get("url", ""),
            "method": request.get("method", ""),
            "url": request.get("url", ""),
            "headers": request.get("headers", []),
            "body": request.get("postData", {})
        }

        endpoints.append(endpoint)

    return {
        "type": "har",
        "endpoints": endpoints
    }