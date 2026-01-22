# Use Go 1.24 with automatic toolchain updates
FROM golang:1.24 AS builder

# Set working directory inside the container
WORKDIR /app

# Install the OpenTelemetry Collector Builder
RUN --mount=type=cache,target=/root/.cache/go-build \
  --mount=type=cache,target=/go/pkg/mod \
  go install go.opentelemetry.io/collector/cmd/builder@v0.142.0

# Copy your builder config
COPY builder-config.yaml .

# Enable more verbose output from the builder
ENV BUILDER_DEBUG=1

ENV CGO_ENABLED=0 GOOS=linux GOARCH=amd64

# Run the builder with extra verbosity and examine the output
RUN --mount=type=cache,target=/root/.cache/go-build \
  --mount=type=cache,target=/go/pkg/mod \
  builder --config builder-config.yaml

# Use a minimal base image
FROM alpine:latest

# Install required system dependencies
RUN apk add --no-cache ca-certificates

# Create config directory for Prometheus scraper targets file
RUN mkdir -p /etc/pdot
VOLUME ["/etc/pdot"]

# Set the working directory
WORKDIR /otel

# Copy the built binary from the builder stage
COPY --from=builder /app/dist/otelcol /otel/otelcol

# Copy all configuration files
COPY configs/ /otel/configs/

# Expose necessary ports
EXPOSE 4317 4318 8126 9090

RUN chmod +x /otel/otelcol

# Run the OpenTelemetry Collector
# No default config - user must specify one via --config flag
ENTRYPOINT ["/otel/otelcol"]
