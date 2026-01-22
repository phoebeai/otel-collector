# Using PDOT for Prometheus Federation

PDOT can scrape metrics from other Prometheus servers using the `/federate` endpoint. This enables hierarchical monitoring setups where PDOT aggregates metrics from multiple Prometheus instances, or selective metric forwarding from existing Prometheus servers to Phoebe.

**Config file:** `/otel/configs/prometheus-federation.yaml`

## When to use Federation

| Scenario | Use Federation |
|----------|----------------|
| Aggregate metrics from multiple Prometheus servers | Yes |
| Forward specific metrics from Prometheus to Phoebe | Yes |
| Scrape application `/metrics` endpoints directly | No (use [scraper](prometheus.md)) |
| Have Prometheus push metrics to PDOT | No (use [remote write](prometheusremotewrite.md)) |

Use **federation** when you have existing Prometheus servers and want to:
- Collect specific metrics from them into Phoebe
- Create a hierarchical monitoring architecture
- Gradually migrate from Prometheus to PDOT

## Requirements

- PDOT with the prometheusreceiver (included in standard builds)
- One or more Prometheus servers with the `/federate` endpoint enabled
- A federation targets file listing Prometheus servers to scrape

## Configuration

### Federation Targets File

Create a targets file at `/etc/pdot/federation.yaml` listing the Prometheus servers to federate from:

```yaml
- targets:
    - "prometheus-1:9090"
  labels:
    "__param_match[]": '{job="my-service"}'
    prometheus_server: prom-1
    env: production

- targets:
    - "prometheus-2:9090"
  labels:
    "__param_match[]": '{job="another-service"},{__name__=~"up|process_.*"}'
    prometheus_server: prom-2
    env: staging
```

Each target group has:

- `targets`: List of Prometheus server `host:port` addresses
- `labels.__param_match[]`: **Required.** Match selector(s) for the federation endpoint
- `labels.*`: Optional custom labels added to all federated metrics

### Match Selectors

The `__param_match[]` label specifies which metrics to federate. This is converted to a `match[]` query parameter when scraping the `/federate` endpoint.

**Single selector:**
```yaml
- targets:
    - "prometheus:9090"
  labels:
    "__param_match[]": '{job="my-service"}'
```

**Multiple selectors (comma-separated):**
```yaml
- targets:
    - "prometheus:9090"
  labels:
    "__param_match[]": '{job="service-a"},{job="service-b"},{__name__=~"http_.*"}'
```

Multiple selectors are OR'd together—metrics matching any selector are returned.

### Common Match Patterns

| Pattern | Description |
|---------|-------------|
| `{job="my-service"}` | All metrics for a specific job |
| `{__name__=~"http_.*"}` | Metrics matching a name pattern |
| `{job="service-a"},{job="service-b"}` | Multiple jobs |
| `{__name__=~"job:.*"}` | Recording rules only |
| `{__name__=~".*_total"}` | All counter metrics |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_PROMETHEUS_FEDERATION_TARGETS_FILE` | `/etc/pdot/federation.yaml` | Path to federation targets file |
| `OTEL_PROMETHEUS_SCRAPE_INTERVAL` | `15s` | How often to scrape (shared with regular scraper) |
| `OTEL_PROMETHEUS_SCRAPE_TIMEOUT` | `10s` | Timeout for each scrape (shared with regular scraper) |

### Hot Reload

The federation targets file is automatically reloaded every 30 seconds. You can add or remove Prometheus servers without restarting PDOT.

### Metric Filtering

PDOT's federation receiver is configured to automatically drop internal Prometheus metrics (`prometheus_*`) to avoid noise in your observability backend. This filtering is applied via `metric_relabel_configs`.

## Use Cases

### Hierarchical Monitoring

Aggregate metrics from regional Prometheus servers:

```yaml
- targets:
    - "prometheus-us-east.internal:9090"
  labels:
    "__param_match[]": '{__name__=~"job:.*"}'
    region: us-east

- targets:
    - "prometheus-us-west.internal:9090"
  labels:
    "__param_match[]": '{__name__=~"job:.*"}'
    region: us-west

- targets:
    - "prometheus-eu.internal:9090"
  labels:
    "__param_match[]": '{__name__=~"job:.*"}'
    region: eu
```

### Selective Metric Forwarding

Forward only specific metrics from Prometheus to Phoebe:

```yaml
- targets:
    - "prometheus:9090"
  labels:
    "__param_match[]": '{job="critical-service"},{__name__=~"error_.*|latency_.*"}'
```

### Multi-Team Prometheus Servers

Federate from team-specific Prometheus instances:

```yaml
- targets:
    - "prometheus-backend.backend-team:9090"
  labels:
    "__param_match[]": '{namespace="backend"}'
    team: backend

- targets:
    - "prometheus-frontend.frontend-team:9090"
  labels:
    "__param_match[]": '{namespace="frontend"}'
    team: frontend
```

### Match Selector Required

Every target must have a `__param_match[]` label. The federation endpoint returns an error if no match selector is provided.

## Known Limitations

### Metric Type Support

| Metric Type | Supported |
|-------------|-----------|
| Counter | Yes |
| Gauge | Yes |
| Histogram (Native) | Yes |
| Histogram (Classic) | No |
| Summary | No |

### No TLS

The initial implementation supports HTTP only. HTTPS Prometheus servers cannot be scraped.

### No Authentication

Basic auth and bearer token authentication are not supported in this version. Prometheus servers must be accessible without authentication.

## Docker Run Example

```bash
docker run --rm \
  -v ./federation.yaml:/etc/pdot/federation.yaml:ro \
  -e PHOEBE_API_KEY=${PHOEBE_API_KEY} \
  pdot --config /otel/configs/prometheus-federation.yaml
```

## Docker Compose Example

```yaml
services:
  pdot:
    image: your-pdot-image
    command: ["--config", "/otel/configs/prometheus-federation.yaml"]
    volumes:
      - ./federation.yaml:/etc/pdot/federation.yaml:ro
    environment:
      OTEL_PROMETHEUS_SCRAPE_INTERVAL: 15s
      PHOEBE_API_KEY: ${PHOEBE_API_KEY}
```

See the [examples/prometheusfederation](../examples/prometheusfederation/) directory for a complete working example.

## References

- [Prometheus Federation Documentation](https://prometheus.io/docs/prometheus/latest/federation/)
- [OpenTelemetry Prometheus Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/prometheusreceiver)
- [Prometheus Match Selector Syntax](https://prometheus.io/docs/prometheus/latest/querying/basics/#instant-vector-selectors)
