from abss.core.models import (
    ForecastFeatures,
    ForecastPoint,
    ForecastResult,
    ForecastTrainingSample,
)


def test_forecast_point() -> None:
    point = ForecastPoint(
        horizon=1,
        revenue=110_000,
        profit=22_000,
        cash=55_000,
        inventory=9_000,
        market_share=0.16,
    )

    assert point.horizon == 1
    assert point.revenue == 110_000
    assert point.profit == 22_000
    assert point.cash == 55_000
    assert point.inventory == 9_000
    assert point.market_share == 0.16


def test_forecast_result() -> None:
    points = [
        ForecastPoint(
            horizon=1,
            revenue=110_000,
            profit=22_000,
            cash=55_000,
            inventory=9_000,
            market_share=0.16,
        ),
        ForecastPoint(
            horizon=2,
            revenue=120_000,
            profit=24_000,
            cash=60_000,
            inventory=8_500,
            market_share=0.17,
        ),
    ]

    result = ForecastResult(
        cycle_id=1,
        horizon=2,
        points=points,
        model_version="test-model-v1",
    )

    assert result.cycle_id == 1
    assert result.horizon == 2
    assert len(result.points) == 2
    assert result.points[0].horizon == 1
    assert result.points[1].horizon == 2
    assert result.model_version == "test-model-v1"


def test_forecast_result_defaults_to_empty_points() -> None:
    result = ForecastResult(
        cycle_id=1,
        horizon=4,
        model_version="test-model-v1",
    )

    assert result.points == []

def test_forecast_training_sample() -> None:
    features = ForecastFeatures(
        revenue=100_000,
        profit=20_000,
        cash=50_000,
        inventory=10_000,
        employees=100,
        market_share=0.15,
        demand_index=1.1,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
        event_count=0.0,
        total_event_severity=0.0,
        high_inflation_event=0.0,
        high_competition_event=0.0,
        low_demand_event=0.0,
        demand_surge_event=0.0,
        cash_constraint_event=0.0,
    )

    target = ForecastPoint(
        horizon=1,
        revenue=110_000,
        profit=22_000,
        cash=55_000,
        inventory=9_000,
        market_share=0.16,
    )

    sample = ForecastTrainingSample(
        features=features,
        target=target,
    )

    assert sample.features.revenue == 100_000
    assert sample.target.revenue == 110_000
    assert sample.target.horizon == 1