import json
import random

from flask import Flask
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

quotes = [
    "Strive not to be a success, but rather to be of value. - Albert Einstein",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "The Marleys were dead to begin with. - Gonzo the Great, 'The Muppet Christmas Carol'",
]

# Counter: total requests
REQUEST_COUNT = Counter(
    "quote_app_requests_total",
    "Total number of requests to the quote app",
    ["quote_index"],
)

# Gauge: current number of available quotes
QUOTES_AVAILABLE = Gauge(
    "quote_app_quotes_available",
    "Number of quotes available in the app",
)
QUOTES_AVAILABLE.set(len(quotes))

# Histogram: request latency (simulated)
REQUEST_LATENCY = Histogram(
    "quote_app_request_latency_seconds",
    "Request latency in seconds",
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)


@app.route("/")
def index():
    with REQUEST_LATENCY.time():
        index = random.randint(0, len(quotes) - 1)
        REQUEST_COUNT.labels(quote_index=str(index)).inc()
        return json.dumps({"index": index, "quote": quotes[index]}) + "\n"


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8089)
