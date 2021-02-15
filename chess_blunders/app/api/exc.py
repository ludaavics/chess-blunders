from requests import HTTPError


def requests_http_error_handler(exc: HTTPError):
    try:
        response_body = exc.response.json()
    except ValueError:
        response_body = exc.response.text

    status_code = exc.response.status_code if exc.response.status_code < 500 else 503
    return {
        "statusCode": status_code,
        "body": {
            "error": {
                "type": "ThirdPartyRequestError",
                "request": {
                    "url": exc.response.request.url,
                    "method": exc.response.request.method,
                    "body": exc.response.request.body,
                },
                "response": {
                    "url": exc.response.url,
                    "status_code": exc.response.status_code,
                    "body": response_body,
                },
            },
        },
    }
