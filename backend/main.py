import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from httpx import HTTPError

from schemas import ProductsAnalyticsResponse, UsersResponse
from services import get_products_analytics, get_users_data

app = FastAPI(title="JTA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPError)
async def upstream_unreachable(request: Request, exc: HTTPError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": "Could not reach DummyJSON"})


@app.exception_handler(json.JSONDecodeError)
async def upstream_bad_payload(request: Request, exc: json.JSONDecodeError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": "DummyJSON returned an invalid response"})


@app.get("/api/users", response_model=UsersResponse)
async def users():
    return await get_users_data()


@app.get("/api/products/analytics", response_model=ProductsAnalyticsResponse)
async def products():
    return await get_products_analytics()
