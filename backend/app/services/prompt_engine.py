import json


def build_prompt(parsed_apis, config, patterns):

    prompt = f"""
You are an expert JMeter performance testing engineer.

Your task is to analyze API endpoints and generate a structured JSON test plan.

IMPORTANT RULES:
- Return ONLY valid JSON
- Do NOT return XML
- Do NOT return markdown
- Do NOT add explanations
- Response must be parseable using json.loads()

Load Configuration:
- Users: {config.users}
- Ramp-up: {config.ramp_up}
- Duration: {config.duration}
- Think Time: {config.think_time}

Testing Requirements:
- Generate realistic API test flow
- Preserve request sequence
- Include all endpoints
- Preserve headers
- Preserve request payloads
- Use ${{username}} and ${{password}} variables
- Use ${{jwt_token}} for protected APIs
- Add assert_response for important APIs
- Login/auth APIs should extract tokens
"""

    if patterns["jwt"]:

        prompt += """
- APIs use JWT authentication
- Protected APIs must reuse extracted JWT token
"""

    if patterns["auth"]:

        prompt += """
- Preserve Authorization headers
"""

    if patterns["session"]:

        prompt += """
- Preserve session continuity
"""

    if patterns["cookie"]:

        prompt += """
- Preserve cookies across requests
"""

    prompt += """

API ENDPOINTS:
"""

    for ep in parsed_apis["endpoints"]:

        prompt += f"""

----------------------------------------
Endpoint Name: {ep['name']}

Method: {ep['method']}

URL: {ep['url']}
"""

        if ep["headers"]:

            prompt += "\nHeaders:\n"

            for header in ep["headers"]:

                key = header.get("key", "") or header.get("name", "")
                value = header.get("value", "")

                prompt += f"- {key}: {value}\n"

        if ep["body"]:

            prompt += f"""

Body:
{json.dumps(ep["body"], indent=2)}
"""

    prompt += f"""

RETURN JSON IN THIS EXACT FORMAT:

{{
  "thread_group": {{
    "users": {config.users},
    "ramp_up": {config.ramp_up},
    "duration": {config.duration},
    "think_time": {config.think_time}
  }},

  "requests": [
    {{
      "name": "Login API",

      "method": "POST",

      "url": "https://api.example.com/login",

      "headers": {{
        "Content-Type": "application/json"
      }},

      "body": {{
        "username": "${{username}}",
        "password": "${{password}}"
      }},

      "extract_token": true,

      "assert_response": "success"
    }},

    {{
      "name": "Get Profile",

      "method": "GET",

      "url": "https://api.example.com/profile",

      "headers": {{
        "Authorization": "Bearer ${{jwt_token}}"
      }}
    }}
  ]
}}

IMPORTANT:
- Return ONLY valid JSON
- No markdown
- No explanations
"""

    return prompt