# 2. Use hexagonal architecture

Date: 2025-03-29

## Status

Accepted

## Context

We must have clean design perception. There multiple possibilities. For a small project like this one there are no
needs for any sophisticated architecture. However, I anticipate that project can grow large in the future and I want
to have clean boundaries on parts of the code.

Considered options:

Layered architecture - very common architecture pattern, however it falls down when we to change the lowest layer,
database. Good option, but I want to present dependency inversion principle :)

Hexagonal architecture - is being known nowadays. Earlier was known as onion architecture. Is the best when we have
large application and business logic.

No architecture - just straightforward implementation without given boundaries. Would be good fit when we don't have
dependency on coingecko and needed only pure crud operation.

## Decision

Use Hexagonal architecture

## Consequences

Code is well-structured. Maybe a bit confusing for people who don't know dependency inversion principle. Small
presentation or workshop might be needed.
