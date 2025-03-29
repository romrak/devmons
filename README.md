# Devmons

This is implementation of homework given from Devmons/Crypkit

## Assignment

The assignment was given in [PDF file](crud_api.pdf)

### Breakdown analysis

I analysed the assignment and decided to do the following things:

- Use FastAPI and python async
- Use SqlAlchemy and alembic
- Do a TDD with unit, acceptance and integration tests
- Describe in readme files all decisions
- Describe in readme files architecture and code design
- Use hexagonal architecture
- Use open telemetry for observability, with Prometheus, Grafana and add some dashboard
- Describe possible SLA, SLI, SLO
- Use github CI/CD pipelines
- Use ruff and mypy for linting
- Use conventional commits
- Use dockerfile with multistage and docker compose
- Write helm charts for kubernetes
- Generate openapi documentation using FastAPI
- Think about further improvements


## Further improvements 

We can do:

- Load testing with Locust
- Add authentication and authorization (for example with keycloack and JWT tokens)
- Add ratelimiting
- Add Graphql support and separate reading from writing (CQRS)
- Alternatives to background tasks (fast api background tasks / k8s cron jobs with entrypoints)