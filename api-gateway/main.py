import os

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse


def generate_operation_id(route):
    methods = "_".join(sorted(route.methods))
    path = (
        route.path_format
        .replace("/", "_")
        .replace("{", "")
        .replace("}", "")
        .replace(":", "_")
    )

    return f"{methods}{path}"


app = FastAPI(
    title="API Gateway",
    generate_unique_id_function=generate_operation_id
)


USER_SERVICE_URL = os.getenv(
    "USER_SERVICE_URL",
    "http://localhost:8001"
)

NOTIFICATION_SERVICE_URL = os.getenv(
    "NOTIFICATION_SERVICE_URL",
    "http://localhost:8002"
)


async def forward_request(request: Request, target_url: str):
    body = await request.body()

    headers = dict(request.headers)
    headers.pop("host", None)

    query_params = request.url.query

    if query_params:
        target_url = f"{target_url}?{query_params}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body
            )

        response_headers = {
            key: value
            for key, value in response.headers.items()
            if key.lower() not in {
                "content-length",
                "transfer-encoding",
                "connection"
            }
        }

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=response_headers,
            media_type=response.headers.get("content-type")
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={
                "detail": "Service temporarily unavailable"
            }
        )


@app.get("/")
def health_check():
    return {
        "service": "API Gateway",
        "status": "running"
    }


@app.api_route(
    "/api/users/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def users(request: Request, path: str):
    target_url = f"{USER_SERVICE_URL}/users/{path}"

    return await forward_request(
        request,
        target_url
    )


@app.api_route(
    "/api/notifications/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def notifications(request: Request, path: str):
    target_url = f"{NOTIFICATION_SERVICE_URL}/notifications/{path}"

    return await forward_request(
        request,
        target_url
    )


@app.api_route(
    "/api/notifications",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def notifications_root(request: Request):
    target_url = f"{NOTIFICATION_SERVICE_URL}/notifications"

    return await forward_request(
        request,
        target_url
    )