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

4. Check your local HyperDX (a local Otel collector and UI), you should see the `quote_app.request` metric being ingested. It's at <http://localhost:8080>.
