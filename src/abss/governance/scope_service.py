from abss.core.models import CompanyState, MarketState, Scope, SimulationEvent


class ScopeService:
    def build_scope(
        self,
        cycle_id: str,
        company_state: CompanyState,
        market_state: MarketState,
        events: list[SimulationEvent],
    ) -> Scope:
        objectives = [
            "Maintain financial stability",
            "Optimize business performance",
        ]

        hard_constraints: dict[str, object] = {}

        if company_state.cash <= 0:
            hard_constraints["cash_constraint"] = True

        if company_state.inventory <= 0:
            hard_constraints["inventory_constraint"] = True

        if market_state.competitor_pressure >= 0.70:
            hard_constraints["high_competition"] = True

        assumptions = {
            "demand_index": market_state.demand_index,
            "inflation_rate": market_state.inflation_rate,
            "interest_rate": market_state.interest_rate,
            "competitor_pressure": market_state.competitor_pressure,
            "seasonality_index": market_state.seasonality_index,
            "active_events": [event.event_type for event in events],
        }

        available_resources = {
            "cash": company_state.cash,
            "inventory": company_state.inventory,
            "employees": float(company_state.employees),
        }

        success_criteria = {
            "maintain_positive_cash": True,
            "avoid_unresolved_constraints": True,
        }

        allowed_decision_space = [
            "pricing",
            "marketing",
            "inventory",
            "hiring",
            "cost_management",
            "capital_allocation",
        ]

        regulatory_limits: dict[str, object] = {}

        return Scope(
            cycle_id=cycle_id,
            objectives=objectives,
            hard_constraints=hard_constraints,
            available_resources=available_resources,
            regulatory_limits=regulatory_limits,
            assumptions=assumptions,
            success_criteria=success_criteria,
            allowed_decision_space=allowed_decision_space,
        )