import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .routers import games

app = FastAPI()


@app.get("/")
async def root():
    exclude_paths = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]
    return [
        {"path": route.path} for route in app.routes if route.path not in exclude_paths
    ]


app.include_router(games.router)


# ------------------------------------------------------------------------------------ #
#                                  Exceptions Handling                                 #
# ------------------------------------------------------------------------------------ #
@app.exception_handler(requests.HTTPError)
async def requests_http_error_handler(request: Request, exc: requests.HTTPError):
    try:
        response_body = exc.response.json()
    except ValueError:
        response_body = exc.response.text

    status_code = exc.response.status_code if exc.response.status_code < 500 else 503
    return JSONResponse(
        status_code=status_code,
        content={
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
    )
