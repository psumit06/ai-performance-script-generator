def compare_apis(old_apis, new_apis):

    changes = []

    old_endpoints = {
        ep["url"]: ep
        for ep in old_apis["endpoints"]
    }

    new_endpoints = {
        ep["url"]: ep
        for ep in new_apis["endpoints"]
    }

    # NEW ENDPOINTS
    for url in new_endpoints:

        if url not in old_endpoints:

            changes.append({
                "type": "NEW_ENDPOINT",
                "url": url
            })

    # REMOVED ENDPOINTS
    for url in old_endpoints:

        if url not in new_endpoints:

            changes.append({
                "type": "REMOVED_ENDPOINT",
                "url": url
            })

    # MODIFIED ENDPOINTS
    for url in old_endpoints:

        if url in new_endpoints:

            old_method = old_endpoints[url]["method"]

            new_method = new_endpoints[url]["method"]

            if old_method != new_method:

                changes.append({
                    "type": "METHOD_CHANGED",
                    "url": url,
                    "old": old_method,
                    "new": new_method
                })

            # HEADER DIFFS
            old_headers = old_endpoints[url].get(
                "headers",
                []
            )

            new_headers = new_endpoints[url].get(
                "headers",
                []
            )

            if old_headers != new_headers:

                changes.append({
                    "type": "HEADERS_CHANGED",
                    "url": url
                })

            # BODY DIFFS
            old_body = old_endpoints[url].get(
                "body",
                {}
            )

            new_body = new_endpoints[url].get(
                "body",
                {}
            )

            if old_body != new_body:

                changes.append({
                    "type": "BODY_CHANGED",
                    "url": url
                })

    return changes