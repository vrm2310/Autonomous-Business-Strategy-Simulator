from abss.core.models import CompanyState, MarketState, SimulationEvent


class EventGeneratorService:
    def generate_events(
        self,
        company_state: CompanyState,
        market_state: MarketState,
    ) -> list[SimulationEvent]:
        events: list[SimulationEvent] = []

        if market_state.inflation_rate >= 0.07:
            events.append(
                SimulationEvent(
                    event_id="high_inflation",
                    event_type="HIGH_INFLATION",
                    severity=min(market_state.inflation_rate / 0.10, 1.0),
                    description="Inflation is elevated and may increase operating costs.",
                ),
            )

        if market_state.competitor_pressure >= 0.70:
            events.append(
                SimulationEvent(
                    event_id="high_competition",
                    event_type="HIGH_COMPETITION",
                    severity=market_state.competitor_pressure,
                    description="Competitive pressure is elevated.",
                ),
            )

        if market_state.demand_index <= 0.80:
            events.append(
                SimulationEvent(
                    event_id="low_demand",
                    event_type="LOW_DEMAND",
                    severity=min((1.0 - market_state.demand_index) / 0.50, 1.0),
                    description="Market demand is below the normal level.",
                ),
            )

        if market_state.demand_index >= 1.20:
            events.append(
                SimulationEvent(
                    event_id="demand_surge",
                    event_type="DEMAND_SURGE",
                    severity=min((market_state.demand_index - 1.0) / 0.50, 1.0),
                    description="Market demand is significantly above the normal level.",
                ),
            )

        if company_state.cash <= 0:
            events.append(
                SimulationEvent(
                    event_id="cash_constraint",
                    event_type="CASH_CONSTRAINT",
                    severity=1.0,
                    description="The company has no available cash.",
                ),
            )

        return events