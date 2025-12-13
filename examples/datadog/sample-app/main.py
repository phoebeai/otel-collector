import json
import random
from os import environ

from datadog import initialize
from datadog.dogstatsd.base import statsd
from flask import Flask

app = Flask(__name__)

quotes = [
    "Strive not to be a success, but rather to be of value. - Albert Einstein",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "The Marleys were dead to begin with. - Gonzo the Great, 'The Muppet Christmas Carol'",
]

statsd_host = environ.get("STATSD_HOST", "localhost")
statsd_port = int(environ.get("STATSD_PORT", 8125))
dd_options = {
    "statsd_host": statsd_host,
    "statsd_port": statsd_port,
}
initialize(**dd_options)


@app.route("/")
def index():
    index = random.randint(0, len(quotes) - 1)
    statsd.increment("quote_app.request", tags=[f"quote_index:{index}"])
    return json.dumps({"index": index, "quote": quotes[index]}) + "\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
