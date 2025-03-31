from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics

from . import crypto

app = FastAPI()

app.include_router(crypto.router)
Instrumentator(
    excluded_handlers=["/metrics"],
).add(
    metrics.latency(
        metric_name="http_request_duration_seconds",
        buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0),  # Define histogram buckets
    )
).instrument(app).expose(app)
