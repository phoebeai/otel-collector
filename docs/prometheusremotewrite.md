# Using PDOT to receive Prometheus Remote Write metrics

You can configure Prometheus to send metrics to PDOT via the [Remote Write 2.0](https://prometheus.io/docs/specs/prw/remote_write_spec_2_0/) protocol. PDOT will forward these metrics to Phoebe.

## Requirements

- **Prometheus 3.8.0 or later** - Required due to wire-protocol changes in the Remote Write 2.0 protocol
- PDOT listens on port 9090 by default for Prometheus Remote Write

## Prometheus Configuration

Start Prometheus with the metadata WAL feature enabled:

```bash
prometheus --enable-feature=metadata-wal-records
```

Add the following to your `prometheus.yml`:

```yaml
remote_write:
  - url: "http://pdot:9090/api/v1/write"
    protobuf_message: "io.prometheus.write.v2.Request"
```

- Change `pdot` to whatever hostname you have assigned to the PDOT container
- If you don't want to use port 9090, you can change this by setting `OTEL_PROMETHEUS_REMOTE_WRITE_PORT` on the PDOT container

## Complete Prometheus Configuration Example

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

remote_write:
  - url: "http://pdot:9090/api/v1/write"
    protobuf_message: "io.prometheus.write.v2.Request"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "my-application"
    static_configs:
      - targets: ["my-app:8000"]
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_PROMETHEUS_REMOTE_WRITE_PORT` | `9090` | Port for the Prometheus Remote Write receiver |

## Known Limitations

The `prometheusremotewritereceiver` is in **alpha** status and has the following limitations:

- **No Summary metrics** - Summaries are unsupported due to atomicity concerns across multiple remote-write requests
- **No Classic Histograms** - Only native histograms are supported
- **Cache limitations** - Uses a hardcoded 1000-entry LRU cache for resource metrics; cache is lost on restart

## References

- [Prometheus Remote Write 2.0 Specification](https://prometheus.io/docs/specs/prw/remote_write_spec_2_0/)
- [Prometheus Remote Write Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)
- [OpenTelemetry Prometheus Remote Write Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/prometheusremotewritereceiver)
