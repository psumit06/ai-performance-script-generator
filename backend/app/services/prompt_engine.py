def build_prompt(api_spec, config, patterns):

    prompt = f"""
Convert this API specification into a valid JMeter JMX test plan.

Users: {config.users}
Ramp-up: {config.ramp_up}
Duration: {config.duration}

Requirements:
- Add HTTP samplers
- Add assertions
"""

    if patterns["jwt"]:
        prompt += "\n- Add JWT correlation"

    if patterns["auth"]:
        prompt += "\n- Handle Authorization headers"

    if patterns["session"]:
        prompt += "\n- Add session handling"

    prompt += f"""

API SPEC:
{api_spec}

Output ONLY XML.
"""

    return prompt