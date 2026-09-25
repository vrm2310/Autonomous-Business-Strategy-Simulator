import torch

from abss.core.models import ForecastFeatures, ForecastPoint
from abss.forecasting.artifact import ForecastArtifact
from abss.forecasting.model import ForecastMLP
from abss.forecasting.preprocessing import ForecastPreprocessor
from abss.forecasting.service import ForecastService


def create_test_artifact() -> ForecastArtifact:
    model = ForecastMLP()

    preprocessor = ForecastPreprocessor()

    train_features = [
        [1.0] * 18,
        [2.0] * 18,
        [3.0] * 18,
    ]

    train_targets = [
        [100.0, 20.0, 50.0, 10.0, 0.10],
        [200.0, 40.0, 100.0, 20.0, 0.20],
        [300.0, 60.0, 150.0, 30.0, 0.30],
    ]

    preprocessor.fit_transform(
        train_features,
        train_targets,
        [[1.5] * 18],
        [[150.0, 30.0, 75.0, 15.0, 0.15]],
    )

    return ForecastArtifact(
        model=model,
        preprocessor=preprocessor,
        model_version="test",
    )


def test_forecast_service_returns_forecast_point() -> None:
    service = ForecastService(create_test_artifact())

    features = ForecastFeatures(
        revenue=100_000,
        profit=20_000,
        cash=50_000,
        inventory=10_000,
        employees=100,
        market_share=0.15,
        demand_index=1.0,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
        event_count=0,
        total_event_severity=0,
        high_inflation_event=0,
        high_competition_event=0,
        low_demand_event=0,
        demand_surge_event=0,
        cash_constraint_event=0,
    )

    result = service.predict(
        cycle_id=1,
        features=features,
    )

    assert result.cycle_id == 1
    assert result.horizon == 4
    assert result.model_version == "test"
    assert len(result.points) == 4

    point = result.points[0]

    assert point.horizon == 1
    assert isinstance(point.revenue, float)
    assert isinstance(point.profit, float)
    assert isinstance(point.cash, float)
    assert isinstance(point.inventory, float)
    assert isinstance(point.market_share, float)


def test_forecast_service_returns_finite_values() -> None:
    service = ForecastService(create_test_artifact())

    features = ForecastFeatures(
        revenue=100_000,
        profit=20_000,
        cash=50_000,
        inventory=10_000,
        employees=100,
        market_share=0.15,
        demand_index=1.0,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
        event_count=0,
        total_event_severity=0,
        high_inflation_event=0,
        high_competition_event=0,
        low_demand_event=0,
        demand_surge_event=0,
        cash_constraint_event=0,
    )

    result = service.predict(
        cycle_id=1,
        features=features,
    )

    point = result.points[0]

    values = [
        point.revenue,
        point.profit,
        point.cash,
        point.inventory,
        point.market_share,
    ]

    assert all(torch.isfinite(torch.tensor(values)))


def test_forecast_service_updates_features_from_forecast() -> None:
    features = ForecastFeatures(
        revenue=100_000,
        profit=20_000,
        cash=50_000,
        inventory=10_000,
        employees=100,
        market_share=0.15,
        demand_index=1.0,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
        event_count=0,
        total_event_severity=0,
        high_inflation_event=0,
        high_competition_event=0,
        low_demand_event=0,
        demand_surge_event=0,
        cash_constraint_event=0,
    )

    forecast = ForecastPoint(
        horizon=1,
        revenue=110_000,
        profit=22_000,
        cash=55_000,
        inventory=9_000,
        market_share=0.16,
    )

    updated = ForecastService.update_features_from_forecast(
        features,
        forecast,
    )

    assert updated.revenue == 110_000
    assert updated.profit == 22_000
    assert updated.cash == 55_000
    assert updated.inventory == 9_000
    assert updated.market_share == 0.16

    assert updated.employees == features.employees
    assert updated.demand_index == features.demand_index


def test_forecast_service_returns_configured_horizon() -> None:
    service = ForecastService(
        create_test_artifact(),
        forecast_horizon=4,
    )

    features = ForecastFeatures(
        revenue=100_000,
        profit=20_000,
        cash=50_000,
        inventory=10_000,
        employees=100,
        market_share=0.15,
        demand_index=1.0,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
        event_count=0,
        total_event_severity=0,
        high_inflation_event=0,
        high_competition_event=0,
        low_demand_event=0,
        demand_surge_event=0,
        cash_constraint_event=0,
    )

    result = service.predict(
        cycle_id=1,
        features=features,
    )

    assert result.horizon == 4
    assert [point.horizon for point in result.points] == [1, 2, 3, 4]


def test_forecast_service_produces_recursive_horizons() -> None:
    service = ForecastService(
        create_test_artifact(),
        forecast_horizon=4,
    )

    features = ForecastFeatures(
        revenue=100_000,
        profit=20_000,
        cash=50_000,
        inventory=10_000,
        employees=100,
        market_share=0.15,
        demand_index=1.0,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
        event_count=0,
        total_event_severity=0,
        high_inflation_event=0,
        high_competition_event=0,
        low_demand_event=0,
        demand_surge_event=0,
        cash_constraint_event=0,
    )

    result = service.predict(
        cycle_id=1,
        features=features,
    )

    assert len(result.points) == 4

    for first, second in zip(
        result.points,
        result.points[1:],
    ):
        assert first.horizon + 1 == second.horizon


def test_forecast_service_uses_previous_forecast_for_next_horizon() -> None:
    service = ForecastService(
        create_test_artifact(),
        forecast_horizon=4,
    )

    features = ForecastFeatures(
        revenue=100_000,
        profit=20_000,
        cash=50_000,
        inventory=10_000,
        employees=100,
        market_share=0.15,
        demand_index=1.0,
        inflation_rate=0.04,
        interest_rate=0.06,
        competitor_pressure=0.50,
        seasonality_index=1.0,
        event_count=0,
        total_event_severity=0,
        high_inflation_event=0,
        high_competition_event=0,
        low_demand_event=0,
        demand_surge_event=0,
        cash_constraint_event=0,
    )

    result = service.predict(
        cycle_id=1,
        features=features,
    )

    assert len(result.points) == 4

    for previous, current in zip(
        result.points,
        result.points[1:],
    ):
        updated_features = (
            ForecastService.update_features_from_forecast(
                features,
                previous,
            )
        )

        assert updated_features.revenue == previous.revenue
        assert updated_features.profit == previous.profit
        assert updated_features.cash == previous.cash
        assert updated_features.inventory == previous.inventory
        assert updated_features.market_share == previous.market_share

        features = updated_features

        assert current.horizon == previous.horizon + 1