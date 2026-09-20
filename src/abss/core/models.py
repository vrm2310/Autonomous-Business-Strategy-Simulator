from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SimulationStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class CompanyState(BaseModel):
    revenue: float = 0.0
    profit: float = 0.0
    cash: float = 0.0
    inventory: float = 0.0
    employees: int = 0
    market_share: float = 0.0


class MarketState(BaseModel):
    demand_index: float = 1.0
    inflation_rate: float = 0.0
    interest_rate: float = 0.0
    competitor_pressure: float = 0.0
    seasonality_index: float = 1.0


class SimulationEvent(BaseModel):
    event_id: str
    event_type: str
    severity: float = Field(ge=0.0, le=1.0)
    description: str


class Scope(BaseModel):
    # Immutable-at-runtime boundary conditions for one simulation cycle.
    model_config = ConfigDict(frozen=True)
    cycle_id: str
    objectives: list[str] = Field(default_factory=list)
    hard_constraints: dict[str, Any] = Field(default_factory=dict)
    available_resources: dict[str, float] = Field(default_factory=dict)
    regulatory_limits: dict[str, Any] = Field(default_factory=dict)
    assumptions: dict[str, Any] = Field(default_factory=dict)
    success_criteria: dict[str, Any] = Field(default_factory=dict)
    allowed_decision_space: list[str] = Field(default_factory=list)


class Proposal(BaseModel):
    proposal_id: str
    cycle_id: str
    decisions: dict[str, Any] = Field(default_factory=dict)


class Vote(BaseModel):
    agent_id: str
    decision: str
    weight: float = Field(gt=0.0)
    confidence: float = Field(ge=0.0, le=1.0)
    justification: str


class VotingResult(BaseModel):
    weighted_approval: float = Field(ge=0.0, le=1.0)
    weighted_rejection: float = Field(ge=0.0, le=1.0)
    votes: list[Vote] = Field(default_factory=lambda: list[Vote]())


class SimulationCycle(BaseModel):
    cycle_id: str
    status: SimulationStatus = SimulationStatus.CREATED
    company_state: CompanyState
    market_state: MarketState
    events: list[SimulationEvent] = Field(default_factory=lambda: list[SimulationEvent]())
    scope: Scope | None = None


class SimulationContext(BaseModel):
    cycle_id: int
    company_id: int
    company_state: CompanyState
    market_state: MarketState
    events: list[SimulationEvent] = Field(
        default_factory=lambda: list[SimulationEvent](),
    )