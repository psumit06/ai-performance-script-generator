from app.services.format_detector import detect_format

from app.services.parser import parse_postman_collection
from app.services.har_parser import parse_har


def parse_api_spec(raw_content):

    detected_format = detect_format(raw_content)

    print("DETECTED FORMAT:", detected_format)

    if detected_format == "postman":
        return parse_postman_collection(raw_content)

    elif detected_format == "har":
        return parse_har(raw_content)

    else:
        raise Exception("Unsupported format")