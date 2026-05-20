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

LOAD CONFIGURATION:
- Users: {config.users}
- Ramp-up: {config.ramp_up}
- Duration: {config.duration}
- Think Time: {config.think_time}

PERFORMANCE ENGINEERING REQUIREMENTS:
- Generate realistic business flows
- Group related APIs into transactions
- Model realistic user journeys
- Preserve request sequence
- Preserve headers
- Preserve request payloads
- Use ${{username}} and ${{password}} variables
- Use ${{jwt_token}} for protected APIs
- Add assert_response for important APIs
- Login/auth APIs should extract tokens
- Assign throughput percentages for each transaction
- Create meaningful transaction names
- Maintain proper request dependencies

MAINTAINABILITY REQUIREMENTS:
- Generate maintainable business flows
- Prefer reusable authentication patterns
- Keep request grouping logically consistent
- Avoid redundant extractors
- Ensure flows are resilient to minor API changes
- Prefer centralized authentication handling
- Minimize duplicated headers where possible

CORRELATION REQUIREMENTS:
- Preserve authentication flow ordering
- Ensure protected APIs use extracted tokens
- Preserve session continuity
- Maintain dependency chains between APIs

OUTPUT REQUIREMENTS:
- Output ONLY valid JSON
- No markdown
- No explanations
- No comments
- Ensure all JSON is properly escaped
"""

    # JWT / Auth Intelligence
    if patterns["jwt"]:

        prompt += """
JWT / AUTH DETECTED:
- APIs use JWT authentication
- Protected APIs must reuse extracted JWT token
- Login transactions should appear first
- Add token extraction where appropriate
"""

    if patterns["auth"]:

        prompt += """
AUTHORIZATION DETECTED:
- Preserve Authorization headers
- Maintain auth propagation across requests
"""

    if patterns["session"]:

        prompt += """
SESSION MANAGEMENT DETECTED:
- Preserve session continuity
- Maintain request ordering
"""

    if patterns["cookie"]:

        prompt += """
COOKIE USAGE DETECTED:
- Preserve cookies across requests
- Use cookie-aware flows
"""

    prompt += """

API ENDPOINTS:
"""

    # ADD PARSED API DETAILS
    for ep in parsed_apis["endpoints"]:

        prompt += f"""

------------------------------------------------
Endpoint Name: {ep['name']}

Method: {ep['method']}

URL: {ep['url']}
"""

        # HEADERS
        if ep["headers"]:

            prompt += "\nHeaders:\n"

            for header in ep["headers"]:

                key = header.get("key", "") or header.get("name", "")

                value = header.get("value", "")

                prompt += f"- {key}: {value}\n"

        # BODY
        if ep["body"]:

            prompt += f"""

Body:
{json.dumps(ep["body"], indent=2)}
"""

    # DAY 12 OUTPUT FORMAT
    prompt += f"""

RETURN JSON IN THIS EXACT FORMAT:

{{
  "thread_group": {{
    "users": {config.users},
    "ramp_up": {config.ramp_up},
    "duration": {config.duration},
    "think_time": {config.think_time}
  }},

  "transactions": [

    {{
      "name": "Login Flow",

      "throughput": 100,

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
        }}
      ]
    }},

    {{
      "name": "User Profile Flow",

      "throughput": 80,

      "requests": [

        {{
          "name": "Get Profile",

          "method": "GET",

          "url": "https://api.example.com/profile",

          "headers": {{
            "Authorization": "Bearer ${{jwt_token}}"
          }},

          "assert_response": "success"
        }}
      ]
    }}

  ]
}}

IMPORTANT:
- Return ONLY valid JSON
- Throughput values should be realistic
- Group related APIs together
- Use transaction names representing business flows
- Keep authentication reusable
- Avoid unnecessary duplication
"""

    return prompt