import json


def normalize_endpoint(
    name,
    method,
    url,
    headers=None,
    body=None
):

    return {
        "name": name,
        "method": method,
        "url": url,
        "headers": headers or [],
        "body": body or {}
    }


def parse_postman_collection(raw_content):

    data = json.loads(raw_content)

    endpoints = []

    items = data.get("item", [])

    for item in items:

        request = item.get("request", {})

        method = request.get("method")

        url_obj = request.get("url", {})

        raw_url = url_obj.get("raw", "")

        headers = request.get("header", [])

        body = request.get("body", {})

        endpoint = normalize_endpoint(
            name=item.get("name"),
            method=method,
            url=raw_url,
            headers=headers,
            body=body
        )

        endpoints.append(endpoint)

    return {
        "type": "postman",
        "endpoints": endpoints
    }