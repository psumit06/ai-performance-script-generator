def build_prompt(parsed_apis, config, patterns):

    prompt = f"""
Generate a production-ready JMeter JMX XML test plan.

Load Configuration:
- Users: {config.users}
- Ramp-up: {config.ramp_up}
- Duration: {config.duration}
- Think Time: {config.think_time}

Requirements:
- Add HTTP Request samplers
- Add Assertions
- Use Transaction Controllers
- Add realistic naming
"""

    # Correlation instructions
    if patterns["jwt"]:
        prompt += "\n- Add JWT token correlation using JSON Extractor"

    if patterns["auth"]:
        prompt += "\n- Handle Authorization headers correctly"

    if patterns["session"]:
        prompt += "\n- Add session handling"

    if patterns["cookie"]:
        prompt += "\n- Add Cookie Manager"

    # Endpoint details
    prompt += "\n\nAPI Endpoints:\n"

    for ep in parsed_apis["endpoints"]:

        prompt += f"""

----------------------------------------
Endpoint Name: {ep['name']}
Method: {ep['method']}
URL: {ep['url']}
"""

        # Headers
        if ep["headers"]:

            prompt += "\nHeaders:\n"

            for header in ep["headers"]:

                key = header.get("key", "")
                value = header.get("value", "")

                prompt += f"- {key}: {value}\n"

        # Body
        if ep["body"]:

            prompt += f"\nBody:\n{ep['body']}\n"

    # Final instructions
    prompt += """

Output Rules:
- Return ONLY valid JMX XML
- Do not return markdown
- Ensure XML is importable into JMeter
"""

    return prompt