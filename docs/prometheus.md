# Using PDOT to scrape Prometheus metrics

PDOT can actively scrape Prometheus metrics endpoints using the `prometheusreceiver`.

**Config file:** `/otel/configs/prometheus-scraper.yaml`

## Configuration

PDOT supports two methods for configuring scrape targets. You can use either method, or both together (targets are merged).

### Option 1: Environment Variable

Pass targets directly via `OTEL_PROMETHEUS_STATIC_CONFIGS` - no file mounting needed:

```bash
docker run --rm \
  -e 'OTEL_PROMETHEUS_STATIC_CONFIGS=[{"targets":["app:8080"],"labels":{"env":"prod"}}]' \
  -e PHOEBE_API_KEY=${PHOEBE_API_KEY} \
  pdot --config /otel/configs/prometheus-scraper.yaml
```

The value is a JSON array of target groups:

```json
[
  {
    "targets": ["app1:8080", "app2:8080"],
    "labels": {"env": "production", "team": "backend"}
  },
  {
    "targets": ["node-exporter:9100"],
    "labels": {"job": "infrastructure"}
  }
]
```

### Option 2: Targets File

Use file-based service discovery by mounting a targets file to `/etc/pdot/targets.yaml`:

```yaml
- targets:
    - "app1:8080"
    - "app2:8080"
  labels:
    env: production
    team: backend

- targets:
    - "node-exporter:9100"
  labels:
    job: infrastructure
```

The targets file is automatically reloaded every 30 seconds. You can add or remove targets without restarting PDOT.

### Hybrid Approach

Both methods can be used together - targets from both sources are merged:

```bash
docker run --rm \
  -v ./targets.yaml:/etc/pdot/targets.yaml:ro \
  -e 'OTEL_PROMETHEUS_STATIC_CONFIGS=[{"targets":["static-host:9090"]}]' \
  -e PHOEBE_API_KEY=${PHOEBE_API_KEY} \
  pdot --config /otel/configs/prometheus-scraper.yaml
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_PROMETHEUS_STATIC_CONFIGS` | `[]` | JSON array of static target configs |
| `OTEL_PROMETHEUS_TARGETS_FILE` | `/etc/pdot/targets.yaml` | Path to targets file |
| `OTEL_PROMETHEUS_SCRAPE_INTERVAL` | `15s` | How often to scrape targets |
| `OTEL_PROMETHEUS_SCRAPE_TIMEOUT` | `10s` | Timeout for each scrape request |
| `OTEL_PROMETHEUS_JOB_NAME` | `default` | Job name for all scraped metrics |

## Known Limitations

### Metric Type Support

| Metric Type | Supported |
|-------------|-----------|
| Counter | Yes |
| Gauge | Yes |
| Histogram (Native) | Yes |
| Histogram (Classic) | No |
| Summary | No |

Classic histograms and summaries are not supported due to atomicity concerns.

### No Authentication and TLS

The initial implementation supports HTTP only. HTTPS endpoints cannot be scraped.
Basic auth and bearer token authentication are not supported in this version.

## Docker Run Examples

### Using environment variable (no file mount)

```bash
docker run --rm \
  -e 'OTEL_PROMETHEUS_STATIC_CONFIGS=[{"targets":["app:8080"],"labels":{"env":"prod"}}]' \
  -e PHOEBE_API_KEY=${PHOEBE_API_KEY} \
  pdot --config /otel/configs/prometheus-scraper.yaml
```

### Using targets file

```bash
docker run --rm \
  -v ./targets.yaml:/etc/pdot/targets.yaml:ro \
  -e PHOEBE_API_KEY=${PHOEBE_API_KEY} \
  pdot --config /otel/configs/prometheus-scraper.yaml
```

## Docker Compose Example

```yaml
services:
  pdot:
    image: your-pdot-image
    command: ["--config", "/otel/configs/prometheus-scraper.yaml"]
    volumes:
      - ./targets.yaml:/etc/pdot/targets.yaml:ro  # Optional, not needed if using env var
    environment:
      # Option 1: Use env var (no file mount needed)
      # OTEL_PROMETHEUS_STATIC_CONFIGS: '[{"targets":["app:8080"]}]'
      # Option 2: Use mounted targets.yaml (shown in volumes above)
      OTEL_PROMETHEUS_SCRAPE_INTERVAL: 15s
      PHOEBE_API_KEY: ${PHOEBE_API_KEY}
```

See the [examples/prometheus](../examples/prometheus/) directory for a complete working example.

## References

- [OpenTelemetry Prometheus Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/prometheusreceiver)
- [Prometheus file_sd configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#file_sd_config)
- [Prometheus exposition format](https://prometheus.io/docs/instrumenting/exposition_formats/)
