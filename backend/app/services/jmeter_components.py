from app.services.xml_helpers import (
    string_prop,
    bool_prop,
    int_prop
)


def build_test_plan():

    xml = ""

    xml += """
<TestPlan guiclass="TestPlanGui"
testclass="TestPlan"
testname="AI Generated Test Plan"
enabled="true">
"""

    xml += string_prop(
        "TestPlan.comments",
        ""
    )

    xml += bool_prop(
        "TestPlan.functional_mode",
        False
    )

    xml += bool_prop(
        "TestPlan.serialize_threadgroups",
        False
    )

    xml += "</TestPlan>"

    return xml


def build_thread_group(users, ramp_up):

    xml = ""

    xml += """
<ThreadGroup guiclass="ThreadGroupGui"
testclass="ThreadGroup"
testname="Thread Group"
enabled="true">
"""

    xml += string_prop(
        "ThreadGroup.on_sample_error",
        "continue"
    )

    xml += """
<elementProp name="ThreadGroup.main_controller"
elementType="LoopController"
guiclass="LoopControlPanel"
testclass="LoopController"
enabled="true">
"""

    xml += bool_prop(
        "LoopController.continue_forever",
        False
    )

    xml += string_prop(
        "LoopController.loops",
        1
    )

    xml += "</elementProp>"

    xml += string_prop(
        "ThreadGroup.num_threads",
        users
    )

    xml += string_prop(
        "ThreadGroup.ramp_time",
        ramp_up
    )

    xml += bool_prop(
        "ThreadGroup.scheduler",
        False
    )

    xml += "</ThreadGroup>"

    return xml


def build_cookie_manager():

    return """
<CookieManager guiclass="CookiePanel"
testclass="CookieManager"
testname="HTTP Cookie Manager"
enabled="true">

<collectionProp name="CookieManager.cookies"/>

<boolProp name="CookieManager.clearEachIteration">
false
</boolProp>

</CookieManager>
"""


def build_csv_dataset():

    return """
<CSVDataSet guiclass="TestBeanGUI"
testclass="CSVDataSet"
testname="CSV User Data"
enabled="true">

<stringProp name="filename">
users.csv
</stringProp>

<stringProp name="variableNames">
username,password
</stringProp>

<stringProp name="delimiter">
,
</stringProp>

<boolProp name="quotedData">
false
</boolProp>

<boolProp name="recycle">
true
</boolProp>

<boolProp name="stopThread">
false
</boolProp>

<stringProp name="shareMode">
shareMode.all
</stringProp>

</CSVDataSet>
"""

def build_transaction_controller(name):

    return f"""
<TransactionController guiclass="TransactionControllerGui"
testclass="TransactionController"
testname="{name}"
enabled="true">

<boolProp name="TransactionController.includeTimers">
false
</boolProp>

<boolProp name="TransactionController.parent">
false
</boolProp>

</TransactionController>
"""

def build_throughput_controller(percent):

    return f"""
<ThroughputController guiclass="ThroughputControllerGui"
testclass="ThroughputController"
testname="Throughput Controller"
enabled="true">

<intProp name="ThroughputController.style">1</intProp>

<boolProp name="ThroughputController.perThread">
false
</boolProp>

<stringProp name="ThroughputController.percentThroughput">
{percent}
</stringProp>

</ThroughputController>
"""