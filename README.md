# Autonomous Business Strategy Simulator (ABSS)

ABSS is a governed multi-agent business strategy simulation system combining
Agentic AI / LLM reasoning, Deep Learning KPI forecasting, game-theoretic
utility functions, dynamic events, immutable per-cycle scope constraints,
iterative executive debate, structured proposals, weighted voting,
convergence detection, controlled termination, strategy execution and
state transitions.

## Architecture rule

The ABSS feature specification and latest architecture diagram are the source
of truth. Implementation must remain synchronized with them.

## Development

```bash
uv sync
uv run uvicorn abss.api.main:app --reload
uv run pytest
uv run ruff check .
uv run pyright
```

## Current milestone

Milestone 0 establishes the project foundation and shared domain contracts.
External LLM providers, databases, forecasting models and agent frameworks
will be wired in incrementally.
