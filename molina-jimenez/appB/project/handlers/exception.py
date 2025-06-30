import json


def handle_exception(exception):
    response = exception.get_response()
    response.content_type = "application/json"
    response.data = json.dumps(
        {
            "message": exception.description,
        }
    )
    return response


def handle_http_exception(exception):
    response = exception.get_response()
    response.content_type = "application/json"
    response.data = json.dumps(
        {
            "code": exception.code,
            "name": exception.name,
            "description": exception.description,
        }
    )
    return response
