from abss.core.models import (
    CompanyState,
    ForecastFeatures,
    MarketState,
    SimulationEvent,
)


class FeatureEngineeringService:
    def build_features(
        self,
        company_state: CompanyState,
        market_state: MarketState,
        events: list[SimulationEvent],
    ) -> ForecastFeatures:
        event_types = {event.event_type for event in events}

        return ForecastFeatures(
            revenue=company_state.revenue,
            profit=company_state.profit,
            cash=company_state.cash,
            inventory=company_state.inventory,
            employees=float(company_state.employees),
            market_share=company_state.market_share,
            demand_index=market_state.demand_index,
            inflation_rate=market_state.inflation_rate,
            interest_rate=market_state.interest_rate,
            competitor_pressure=market_state.competitor_pressure,
            seasonality_index=market_state.seasonality_index,
            event_count=float(len(events)),
            total_event_severity=sum(event.severity for event in events),
            high_inflation_event=float(
                "HIGH_INFLATION" in event_types,
            ),
            high_competition_event=float(
                "HIGH_COMPETITION" in event_types,
            ),
            low_demand_event=float(
                "LOW_DEMAND" in event_types,
            ),
            demand_surge_event=float(
                "DEMAND_SURGE" in event_types,
            ),
            cash_constraint_event=float(
                "CASH_CONSTRAINT" in event_types,
            ),
        )