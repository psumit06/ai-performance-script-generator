import json

from urllib.parse import (
    urlparse,
    parse_qs
)

from app.services.normalized_schema import (
    create_endpoint_schema
)


def parse_postman_collection(content):

    data = json.loads(content)

    endpoints = []

    items = data.get("item", [])

    for item in items:

        request = item.get(
            "request",
            {}
        )

        endpoint = create_endpoint_schema()

        # =========================
        # NAME
        # =========================

        endpoint["name"] = item.get(
            "name",
            "Unnamed Request"
        )

        # =========================
        # METHOD
        # =========================

        endpoint["method"] = request.get(
            "method",
            "GET"
        )

        # =========================
        # URL
        # =========================

        raw_url = request.get(
            "url",
            {}
        )

        if isinstance(raw_url, dict):

            full_url = raw_url.get(
                "raw",
                ""
            )

        else:

            full_url = str(raw_url)

        endpoint["full_url"] = full_url

        parsed = urlparse(full_url)

        endpoint["protocol"] = parsed.scheme

        endpoint["host"] = parsed.hostname or ""

        endpoint["port"] = parsed.port or ""

        endpoint["path"] = parsed.path or "/"

        # =========================
        # QUERY PARAMS
        # =========================

        query_dict = parse_qs(
            parsed.query
        )

        query_params = []

        for key, values in query_dict.items():

            for value in values:

                query_params.append({

                    "key": key,

                    "value": value,

                    "enabled": True
                })

        endpoint["query_params"] = query_params

        # =========================
        # HEADERS
        # =========================

        headers = request.get(
            "header",
            []
        )

        normalized_headers = []

        content_type = ""

        for header in headers:

            key = header.get(
                "key",
                ""
            )

            value = header.get(
                "value",
                ""
            )

            normalized_headers.append({

                "key": key,

                "value": value
            })

            if key.lower() == "content-type":

                content_type = value

        endpoint["headers"] = normalized_headers

        endpoint["content_type"] = content_type

        # =========================
        # BODY
        # =========================

        body = request.get(
            "body",
            {}
        )

        body_mode = body.get(
            "mode",
            ""
        )

        endpoint["body_mode"] = body_mode

        # RAW BODY
        if body_mode == "raw":

            endpoint["raw_body"] = body.get(
                "raw",
                ""
            )

        # FORM DATA
        elif body_mode == "formdata":

            endpoint["form_data"] = body.get(
                "formdata",
                []
            )

        # URL ENCODED
        elif body_mode == "urlencoded":

            endpoint["urlencoded"] = body.get(
                "urlencoded",
                []
            )

        # GRAPHQL
        elif body_mode == "graphql":

            endpoint["graphql"] = body.get(
                "graphql",
                {}
            )

        endpoints.append(endpoint)

    return {

        "type": "postman",

        "endpoints": endpoints
    }