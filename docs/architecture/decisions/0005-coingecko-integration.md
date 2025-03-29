# 5. Coingecko integration

Date: 2025-03-29

## Status

Accepted

## Context

We have to check whether symbol exists in the Coingecko. That is, for each change we have to check it. So we need an
account at Coingecko. There are two options - free demo and paid. Each plan has their limits (
see https://www.coingecko.com/en/api/pricing).

Because of the limits we will cache the values. There is already Redis in the tech stack. It is good enough for us.

## Decision

We use free demo account at Coingecko, for the purpose of this assignment.

We use Redis for caching.

## Consequences

Support the account at Coingecko, later with some price.

Cache data into Redis, however we might not have always the latest data available.