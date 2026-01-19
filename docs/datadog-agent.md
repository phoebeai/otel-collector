# Using PDOT to send data from the Datadog Agent to Phoebe

You can use Datadog's [dual-shipping](https://docs.datadoghq.com/agent/configuration/dual-shipping/?tab=helm) feature to send metrics, logs and traces emitted by the Datadog Agent to both Datadog and Phoebe.

![Basic diagram showing PDOT use for dual-shipping Datadog data](img/pdot-datadog-dual-shipping.png)

## Metrics

Add the following to your Datadog Agent:

```env
DD_ADDITIONAL_ENDPOINTS='{"http://pdot:8226": ["fakeApiKey"]}'
```

- The Datadog Agent requires an API key to be configured, but PDOT doesn't use it, hence the fake value.
- Change `pdot` for whatever hostname you have assigned to the PDOT container
- If you don't want to use port 8226, you can change this by setting `OTEL_DATADOG_RECEIVER_PORT` on the PDOT container.

**Important**: Set the OTEL_RESOURCE_ATTRIBUTES env variable on your PDOT container to match the tags configured on your Datadog Agent. These tags are otherwise lost when forwarding from the Datadog Agent to Phoebe.

Note that Datadog Agent uses the format `tag:value tag:value`, whereas PDOT uses the format `tag=value,tag=value`.

For example, if you have this in your Datadog Agent config:

```env
DD_TAGS="project:phoebe-pdot-demo team:devops"
```

Then add this to your PDOT config:

```env
OTEL_RESOURCE_ATTRIBUTES="project=phoebe-pdot-demo,team=devops"
```

## Logs

```env
DD_LOGS_CONFIG_ADDITIONAL_ENDPOINTS='[{"api_key": "fakeApiKey", "Host": "pdot", "Port": 8126, "use_ssl": false}]'

# The Otel datadogreceiver in PDOT doesn't support the Datadog Agent's connectivity request but we want to use HTTP anyway
DD_LOGS_CONFIG_FORCE_USE_HTTP=true
```

## Traces

```env
DD_APM_ADDITIONAL_ENDPOINTS='{"http://pdot:8226": ["fakeApiKey"]}'
```
