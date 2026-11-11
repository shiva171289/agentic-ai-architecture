# ADR — Parallelization

**Status:** accepted  
**Week:** w04

## Decision

Use `ThreadPoolExecutor` with two workers for policy + order snippet fetch, then existing answer chain.

## When NOT to use

- Step B needs output of step A
- Thread safety issues on shared clients (use async + proper pools in prod)
