# Datadog Agent demo

1. Create a `.env` file (use `.env.example` as your template)
2. Run the stack:

    ```command
    docker compose up -d
    ```

3. Hit <http://localhost:5050> a few times

    ```command
    curl http://localhost:5050
    ```

4. Check your [local HyperDX](http://localhost:8080) (a local Otel collector and UI - follow the prompts to set up a connection and a metrics source on first use). You should see the `quote_app.request` metric being ingested.
