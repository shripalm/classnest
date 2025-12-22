import time
import uuid
import sys
import json
from fastapi import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

# Configure a specific logger for canonical request logs
request_logger = structlog.get_logger("request_canonical")

# Define fields to redact for security
SENSITIVE_HEADERS = {"authorization", "cookie", "x-api-key"}
SENSITIVE_BODY_FIELDS = {"password", "credit_card", "token"}

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Request ID Injection
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # 4. Context-Aware Logger (bind request_id to context)
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        start_time_s = time.time()

        # Log request start
        request_logger.info(
            "Request started",
            log_type="REQUEST_STARTED",
            request_details={
                "http_meta": {
                    "method": request.method,
                    "path": request.url.path,
                    "client_ip": request.client.host if request.client else "unknown",
                },
                "request_headers": {k: v for k, v in request.headers.items() if k.lower() not in SENSITIVE_HEADERS},
            }
        )

        response = await call_next(request)
        
        # Log request finished
        timing_ms = int((time.time() - start_time_s) * 1000)
        
        # Get response body
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        request_logger.info(
            "Request finished",
            log_type="REQUEST_FINISHED",
            response_meta={
                "status_code": response.status_code,
                "response_time_ms": timing_ms,
            }
        )

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
