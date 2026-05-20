import json

from urllib.parse import urlparse

from app.services.jmeter_components import (
    build_test_plan,
    build_thread_group,
    build_cookie_manager,
    build_csv_dataset,
    build_transaction_controller,
    build_throughput_controller
)

from app.services.xml_helpers import (
    string_prop,
    bool_prop
)


def build_jmx(test_plan):

    users = test_plan["thread_group"]["users"]

    ramp_up = test_plan["thread_group"]["ramp_up"]

    think_time = test_plan["thread_group"]["think_time"]

    xml = """<?xml version="1.0" encoding="UTF-8"?>

<jmeterTestPlan version="1.2"
properties="5.0"
jmeter="5.6.3">

<hashTree>
"""

    # TEST PLAN
    xml += build_test_plan()

    xml += "<hashTree>"

    # THREAD GROUP
    xml += build_thread_group(
        users,
        ramp_up
    )

    xml += "<hashTree>"

    # CSV DATASET
    xml += build_csv_dataset()

    xml += "<hashTree/>"

    # COOKIE MANAGER
    xml += build_cookie_manager()

    xml += "<hashTree/>"

    # TRANSACTION LOOP
    for transaction in test_plan["transactions"]:

        transaction_name = transaction["name"]

        throughput = transaction.get(
            "throughput",
            100
        )

        requests = transaction["requests"]

        # TRANSACTION CONTROLLER
        xml += build_transaction_controller(
            transaction_name
        )

        xml += "<hashTree>"

        # THROUGHPUT CONTROLLER
        xml += build_throughput_controller(
            throughput
        )

        xml += "<hashTree>"

        # REQUEST LOOP
        for request in requests:

            parsed_url = urlparse(
                request["url"]
            )

            protocol = parsed_url.scheme

            domain = parsed_url.netloc

            path = parsed_url.path

            headers = request.get(
                "headers",
                {}
            )

            body = request.get(
                "body",
                {}
            )

            body_string = json.dumps(
                body
            )

            # HTTP SAMPLER
            xml += f"""
<HTTPSamplerProxy guiclass="HttpTestSampleGui"
testclass="HTTPSamplerProxy"
testname="{request['name']}"
enabled="true">

<elementProp name="HTTPsampler.Arguments"
elementType="Arguments">

<collectionProp name="Arguments.arguments">

<elementProp name=""
elementType="HTTPArgument">

{bool_prop("HTTPArgument.always_encode", False)}

{string_prop("Argument.value", body_string)}

{string_prop("Argument.metadata", "=")}

</elementProp>

</collectionProp>

</elementProp>

{string_prop("HTTPSampler.domain", domain)}

{string_prop("HTTPSampler.port", "")}

{string_prop("HTTPSampler.protocol", protocol)}

{string_prop("HTTPSampler.path", path)}

{string_prop("HTTPSampler.method", request["method"])}

{bool_prop("HTTPSampler.postBodyRaw", True)}

{bool_prop("HTTPSampler.follow_redirects", True)}

{bool_prop("HTTPSampler.use_keepalive", True)}

</HTTPSamplerProxy>

<hashTree>
"""

            # HEADER MANAGER
            if headers:

                xml += """
<HeaderManager guiclass="HeaderPanel"
testclass="HeaderManager"
testname="HTTP Header Manager"
enabled="true">

<collectionProp name="HeaderManager.headers">
"""

                for key, value in headers.items():

                    xml += f"""
<elementProp name=""
elementType="Header">

{string_prop("Header.name", key)}

{string_prop("Header.value", value)}

</elementProp>
"""

                xml += """
</collectionProp>

</HeaderManager>

<hashTree/>
"""

            # JSON TOKEN EXTRACTOR
            if request.get("extract_token"):

                xml += """
<JSONPostProcessor
guiclass="JSONPostProcessorGui"
testclass="JSONPostProcessor"
testname="Extract JWT Token"
enabled="true">

<stringProp name="JSONPostProcessor.referenceNames">
jwt_token
</stringProp>

<stringProp name="JSONPostProcessor.jsonPathExprs">
$.token
</stringProp>

</JSONPostProcessor>

<hashTree/>
"""

            # RESPONSE ASSERTION
            if request.get("assert_response"):

                xml += """
<ResponseAssertion guiclass="AssertionGui"
testclass="ResponseAssertion"
testname="Response Assertion"
enabled="true">

<collectionProp name="Asserion.test_strings">

<stringProp name="0">
success
</stringProp>

</collectionProp>

<stringProp name="Assertion.test_field">
Assertion.response_data
</stringProp>

<boolProp name="Assertion.assume_success">
false
</boolProp>

<intProp name="Assertion.test_type">2</intProp>

</ResponseAssertion>

<hashTree/>
"""

            # THINK TIME TIMER
            xml += f"""
<ConstantTimer guiclass="ConstantTimerGui"
testclass="ConstantTimer"
testname="Think Time"
enabled="true">

{string_prop(
    "ConstantTimer.delay",
    think_time
)}

</ConstantTimer>

<hashTree/>
"""

            # CLOSE REQUEST HASHTREE
            xml += """
</hashTree>
"""

        # CLOSE THROUGHPUT CONTROLLER HASHTREE
        xml += """
</hashTree>
"""

        # CLOSE TRANSACTION CONTROLLER HASHTREE
        xml += """
</hashTree>
"""

    # CLOSE THREAD GROUP HASHTREE
    xml += """
</hashTree>
"""

    # CLOSE TEST PLAN HASHTREE
    xml += """
</hashTree>
"""

    # CLOSE ROOT HASHTREE
    xml += """
</hashTree>

</jmeterTestPlan>
"""

    return xml