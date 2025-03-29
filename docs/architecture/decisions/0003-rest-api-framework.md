# 3. REST API framework

Date: 2025-03-29

## Status

Accepted

## Context

What framework for REST API we will use? Do we even need or want to use any framework?

Options are:

- no framework - no, please no, is not in the tech stack
- Flask - is in tech stack, no fast enough, doesn't support async
- FastAPI - is in tech stack, fastest, support async, supports dependency injections and pydantic

## Decision

use FastAPI


## Consequences

We are dependant on FastAPI