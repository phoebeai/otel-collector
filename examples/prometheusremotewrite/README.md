# Prometheus Remote Write demo

1. Run the stack:

    ```command
    docker compose up -d
    ```

2. Hit <http://localhost:8000> a few times to generate metrics:

    ```command
    curl http://localhost:8000
    ```

3. Check your [local HyperDX](http://localhost:8080) (a local Otel collector and UI - follow the prompts to set up a connection and a metrics source on first use). You should see the `quote_app_requests_total` metric being ingested.

4. You can also check the Prometheus UI at <http://localhost:9091> to see the scrape targets and remote write status.
