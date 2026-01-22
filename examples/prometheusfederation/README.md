# Prometheus Federation demo

This example demonstrates PDOT federating metrics from a Prometheus server, including both raw metrics and recording rules (pre-aggregated metrics).

## How it works

1. Sample Flask app exposes `/metrics` endpoint with Prometheus metrics
2. Prometheus scrapes the sample app and evaluates recording rules for aggregations
3. PDOT federates specific metrics from Prometheus via `/federate` endpoint
4. Metrics flow to HyperDX for visualization

```
┌─────────────┐     scrape      ┌─────────────┐    federate    ┌─────────────┐     export     ┌─────────────┐
│  Flask App  │ ◄────────────── │ Prometheus  │ ◄───────────── │    PDOT     │ ──────────────►│  HyperDX    │
│  /metrics   │                 │  + rules    │                │ federation  │                │     UI      │
└─────────────┘                 └─────────────┘                └─────────────┘                └─────────────┘
```

## Running the example

1. Start the stack:

    ```bash
    docker compose up -d
    ```

2. Generate some traffic to the sample app:

    ```bash
    for i in {1..20}; do curl -s http://localhost:8089 > /dev/null; sleep 1; done
    ```

3. Open [HyperDX](http://localhost:8080) to view the metrics.

4. Look for these metrics in the metrics explorer:
   - `quote_app_requests_total` - Raw counter from the app
   - `job:quote_app_requests:rate5m` - Recording rule: request rate
   - `job:quote_app_request_latency:p95` - Recording rule: 95th percentile latency

## Files

- `compose.yaml` - Docker Compose stack definition
- `federation.yaml` - PDOT federation targets with match selectors
- `prometheus.yml` - Prometheus configuration for scraping
- `rules.yml` - Prometheus recording rules for metric aggregations

## Recording Rules

This example includes recording rules that pre-aggregate metrics in Prometheus:

| Rule Name | Description |
|-----------|-------------|
| `job:quote_app_requests:rate5m` | Request rate per second (5m window) |
| `job:quote_app_requests_by_endpoint:rate5m` | Request rate by endpoint |
| `job:quote_app_request_latency:avg5m` | Average latency (5m window) |
| `job:quote_app_request_latency:p95` | 95th percentile latency |
| `job:quote_app_request_latency:p99` | 99th percentile latency |
| `job:quote_app_quotes_available:current` | Current quotes available |

Recording rules are federated using the `{__name__=~"job:.*"}` match selector.

## Configuration

The federation targets file (`federation.yaml`) defines which Prometheus servers to federate from and which metrics to collect:

```yaml
- targets:
    - "prometheus:9090"
  labels:
    # Match raw metrics AND recording rules
    __param_match[]: '{job="sample-app"},{__name__=~"job:.*"}'
    prometheus_server: main
    env: development
```

### Match Selector Examples

```yaml
# Single job (raw metrics only)
__param_match[]: '{job="my-service"}'

# Recording rules only (aggregated metrics)
__param_match[]: '{__name__=~"job:.*|instance:.*"}'

# Both raw and aggregated
__param_match[]: '{job="my-service"},{__name__=~"job:.*"}'

# Specific metric types
__param_match[]: '{__name__=~".*_total|.*_bucket"}'
```

## Metric Filtering

PDOT is configured to drop internal Prometheus metrics (`prometheus_*`) to avoid noise. This is done via `metric_relabel_configs` in the receiver configuration.

## Verifying Federation

Check that Prometheus has metrics:
```bash
curl 'http://localhost:9091/api/v1/query?query=up'
```

Check the federation endpoint directly:
```bash
curl 'http://localhost:9091/federate?match[]={job="sample-app"}'
```

Check recording rules are being evaluated:
```bash
curl 'http://localhost:9091/api/v1/query?query=job:quote_app_requests:rate5m'
```
