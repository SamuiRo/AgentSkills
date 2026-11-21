> **Role:** How the system is designed and what not to break · **Audience:** Anyone changing structural or cross-cutting behavior

<!--
This file is for reasoning that's still load-bearing for how the whole
system holds together. A single bounded choice ("why Postgres over Mongo")
belongs in docs/decisions/ instead — put it here only if understanding it is
necessary to safely change anything nearby.
-->

## Overview

<!-- What this system is, in a few sentences, and how its major parts relate. -->

## Data / schema

<!-- Or the equivalent for this project: core data structures, storage
model, how they relate. -->

## Key flows

<!-- The handful of flows that matter most (a request lifecycle, an auth
flow, a job pipeline) — enough to trace a bug without reading every file. -->

## Invariants — what not to break

<!--
The specific things that would silently misbehave if changed carelessly,
and why they're built the way they are. This section is the payoff of the
whole file — write it plainly enough that someone unfamiliar with the
history doesn't reintroduce a bug that was already fixed once.
-->

-

## Trade-offs

<!-- Where this design deliberately gave something up, and what was gained
instead. If a trade-off has enough of its own argument/history to be worth
tracing later, give it its own file in docs/decisions/ and link it here. -->

-
