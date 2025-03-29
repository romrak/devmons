# 6. Who generates id?

Date: 2025-03-29

## Status

Accepted

## Context

We have to decide where to generate ID for our entities.

Possibilities considered:

- DB generation - Hard to test, heavy dependency on DB which is hard to change in the future.
- Generator in the core - Probably the cleanest way, but we need to implement and maintain it.
- Just use uuid4() - Easy to use, already implemented, but we would need to patch usage in tests.
- Require clients to provide it - Not the cleanest way, but in CQRS pretty standard way. 

## Decision

REST API clients must provide ID when using our API.

## Consequences

We have simpler implementation, but there is more heavy weighting on clients now.