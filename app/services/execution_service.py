import ipaddress
import socket
import time
from urllib.parse import urlparse
import httpx
from fastapi import HTTPException
from app.models import APIRequest

def _validate_public_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise HTTPException(status_code=400, detail="Only absolute HTTP(S) URLs are allowed")
    host = parsed.hostname.lower()
    if host in {"localhost", "metadata.google.internal"} or host.endswith(".localhost"):
        raise HTTPException(status_code=400, detail="Target host is not allowed")
    try:
        addresses = socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)
    except socket.gaierror:
        raise HTTPException(status_code=400, detail="Target host could not be resolved")
    for item in addresses:
        address = ipaddress.ip_address(item[4][0])
        if not address.is_global:
            raise HTTPException(status_code=400, detail="Private, local, and reserved network targets are not allowed")

def execute_saved_request(item: APIRequest) -> dict:
    _validate_public_url(item.url)
    try:
        start = time.perf_counter()
        with httpx.Client(timeout=10.0, follow_redirects=False, trust_env=False) as client:
            response = client.request(
                item.method, item.url, headers=item.headers, params=item.params,
                content=item.body, follow_redirects=False,
            )
        elapsed = (time.perf_counter() - start) * 1000
        body = response.text[:100_000]
        return {
            "request_id": item.id, "status_code": response.status_code,
            "elapsed_ms": round(elapsed, 2),
            "response_headers": dict(response.headers),
            "response_body": body,
        }
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Target API timed out")
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Target API request failed: {type(exc).__name__}")
