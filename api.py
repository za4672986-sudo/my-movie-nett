import json
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MovieBox Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_BASE = "https://h5-api.aoneroom.com/wefeed-h5api-bff"
_bearer_token = None

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://moviebox.ph/",
    "Origin": "https://moviebox.ph",
    "X-Client-Info": '{"timezone":"Asia/Dhaka"}',
    "X-Request-Lang": "en",
    "Accept": "application/json"
}

async def get_token():
    global _bearer_token
    if _bearer_token:
        return _bearer_token
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            r = await client.get(f"{API_BASE}/home?host=moviebox.ph", headers=DEFAULT_HEADERS)
            x_user = r.headers.get("x-user")
            if x_user:
                _bearer_token = json.loads(x_user).get("token")
        except:
            pass
    return _bearer_token or ""

@app.get("/api/search")
async def search(q: str = Query(...)):
    token = await get_token()
    headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {token}"} if token else DEFAULT_HEADERS
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(f"{API_BASE}/search/suggest?keyword={q}&host=moviebox.ph", headers=headers)
        return res.json()

@app.get("/api/detail/{slug}")
async def detail(slug: str):
    token = await get_token()
    headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {token}"} if token else DEFAULT_HEADERS
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(f"{API_BASE}/subject/detail?detailPath={slug}&host=moviebox.ph", headers=headers)
        return res.json()
