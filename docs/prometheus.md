# Using PDOT to scrape Prometheus metrics

PDOT can actively scrape Prometheus metrics endpoints using the `prometheusreceiver`.

## Configuration

### Targets File

PDOT uses file-based service discovery. Create a targets file at `/etc/pdot/targets.yaml` (or configure a custom path):

**Config file:** `/otel/configs/prometheus-scraper.yaml`

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

Each target group can have:

- `targets`: List of `host:port` addresses to scrape
- `labels`: Key-value pairs added to all metrics from these targets

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_PROMETHEUS_TARGETS_FILE` | `/etc/pdot/targets.yaml` | Path to targets file |
| `OTEL_PROMETHEUS_SCRAPE_INTERVAL` | `15s` | How often to scrape targets |
| `OTEL_PROMETHEUS_SCRAPE_TIMEOUT` | `10s` | Timeout for each scrape request |

### Hot Reload

The targets file is automatically reloaded every 30 seconds. You can add or remove targets without restarting PDOT.

**Note:** If the targets file is missing or empty, PDOT will start but will not scrape any metrics.

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

## Docker Run Example

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
      - ./targets.yaml:/etc/pdot/targets.yaml:ro
    environment:
      OTEL_PROMETHEUS_SCRAPE_INTERVAL: 15s
      PHOEBE_API_KEY: ${PHOEBE_API_KEY}
```

See the [examples/prometheus](../examples/prometheus/) directory for a complete working example.

## References

- [OpenTelemetry Prometheus Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/prometheusreceiver)
- [Prometheus file_sd configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#file_sd_config)
- [Prometheus exposition format](https://prometheus.io/docs/instrumenting/exposition_formats/)
