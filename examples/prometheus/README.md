# Prometheus Scraper demo

This example demonstrates PDOT actively scraping Prometheus metrics from a sample application, without requiring a separate Prometheus server.

## How it works

1. Sample Flask app exposes `/metrics` endpoint with Prometheus metrics
2. PDOT scrapes the app using file-based service discovery
3. Metrics flow to HyperDX for visualization

```
┌─────────────┐     scrape      ┌─────────────┐     export     ┌─────────────┐
│  Flask App  │ ◄────────────── │    PDOT     │ ──────────────►│  HyperDX    │
│  /metrics   │                 │  scraper    │                │     UI      │
└─────────────┘                 └─────────────┘                └─────────────┘
```

## Running the example

1. Start the stack:

    ```bash
    docker compose up -d
    ```

2. Generate some traffic to the sample app:

    ```bash
    curl http://localhost:8089
    curl http://localhost:8089
    curl http://localhost:8089
    ```

3. Open [HyperDX](http://localhost:8080) to view the metrics. On first use, follow the prompts to set up a connection.

4. Look for the `quote_app_requests_total` metric in the metrics explorer.

## Files

- `compose.yaml` - Docker Compose stack definition
- `targets.yaml` - Prometheus file_sd targets configuration
- `sample-app/` - Flask application exposing /metrics

## Configuration

The targets file (`targets.yaml`) defines which endpoints PDOT scrapes:

```yaml
- targets:
    - "web:8089"
  labels:
    app: quote-demo
    env: development
```

To add more targets, edit `targets.yaml`. PDOT automatically detects changes within 30 seconds.

## Differences from Remote Write example

| Aspect | This example (Scraper) | Remote Write example |
|--------|------------------------|----------------------|
| Prometheus server | Not needed | Required |
| Data flow | PDOT pulls from app | Prometheus pushes to PDOT |
| Configuration | targets.yaml | prometheus.yml |
