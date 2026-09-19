from abss.environment.service import MarketEnvironmentService


def test_get_current_market_state_uses_defaults() -> None:
    service = MarketEnvironmentService()

    state = service.get_current_market_state()

    assert state.demand_index == 1.0
    assert state.inflation_rate == 0.04
    assert state.interest_rate == 0.06
    assert state.competitor_pressure == 0.50
    assert state.seasonality_index == 1.0


def test_get_current_market_state_uses_configured_values() -> None:
    service = MarketEnvironmentService(
        demand_index=1.15,
        inflation_rate=0.05,
        interest_rate=0.07,
        competitor_pressure=0.75,
        seasonality_index=1.20,
    )

    state = service.get_current_market_state()

    assert state.demand_index == 1.15
    assert state.inflation_rate == 0.05
    assert state.interest_rate == 0.07
    assert state.competitor_pressure == 0.75
    assert state.seasonality_index == 1.20