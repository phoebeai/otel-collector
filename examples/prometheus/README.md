# Prometheus Scraper demo

This example demonstrates PDOT actively scraping Prometheus metrics from a sample application, without requiring a separate Prometheus server.

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

PDOT supports two methods for configuring scrape targets (can use one or both):

### Option 1: File-based discovery

The targets file (`targets.yaml`) defines which endpoints PDOT scrapes:

```yaml
- targets:
    - "web:8089"
  labels:
    app: quote-demo
    env: development
```

To add more targets, edit `targets.yaml`. PDOT automatically detects changes within 30 seconds.

### Option 2: Environment variable

Pass targets directly via `OTEL_PROMETHEUS_STATIC_CONFIGS` (no file mounting needed):

```bash
docker run --rm \
  -e 'OTEL_PROMETHEUS_STATIC_CONFIGS=[{"targets":["app:8080"],"labels":{"env":"prod"}}]' \
  -e PHOEBE_API_KEY=your_key \
  pdot:latest --config /otel/configs/prometheus-scraper.yaml
```

### Hybrid approach

Both methods can be used together - targets are merged:

```bash
docker run --rm \
  -v ./targets.yaml:/etc/pdot/targets.yaml:ro \
  -e 'OTEL_PROMETHEUS_STATIC_CONFIGS=[{"targets":["static-host:9090"]}]' \
  -e PHOEBE_API_KEY=your_key \
  pdot:latest --config /otel/configs/prometheus-scraper.yaml
```

## Differences from Remote Write example

| Aspect | This example (Scraper) | Remote Write example |
|--------|------------------------|----------------------|
| Prometheus server | Not needed | Required |
| Data flow | PDOT pulls from app | Prometheus pushes to PDOT |
| Configuration | targets.yaml | prometheus.yml |
