from abss.forecasting.synthetic_data import SyntheticDataGenerator


def test_generate_company_state() -> None:
    generator = SyntheticDataGenerator(seed=42)

    state = generator.generate_company_state()

    assert 80_000 <= state.revenue <= 150_000
    assert 10_000 <= state.profit <= 35_000
    assert 30_000 <= state.cash <= 100_000
    assert 5_000 <= state.inventory <= 20_000
    assert 50 <= state.employees <= 200
    assert 0.08 <= state.market_share <= 0.25


def test_generate_market_state() -> None:
    generator = SyntheticDataGenerator(seed=42)

    state = generator.generate_market_state()

    assert 0.70 <= state.demand_index <= 1.30
    assert 0.02 <= state.inflation_rate <= 0.10
    assert 0.03 <= state.interest_rate <= 0.10
    assert 0.20 <= state.competitor_pressure <= 0.90
    assert 0.80 <= state.seasonality_index <= 1.20


def test_generate_sample_inputs() -> None:
    generator = SyntheticDataGenerator(seed=42)

    company_state, market_state, events = (
        generator.generate_sample_inputs()
    )

    assert company_state.revenue > 0
    assert market_state.demand_index > 0
    assert isinstance(events, list)

def test_generate_future_state() -> None:
    generator = SyntheticDataGenerator(seed=42)

    company_state, market_state, events = (
        generator.generate_sample_inputs()
    )

    future = generator.generate_future_state(
        company_state=company_state,
        market_state=market_state,
        events=events,
    )

    assert future.horizon == 1
    assert future.revenue > 0
    assert future.profit != company_state.profit
    assert future.cash > 0
    assert future.inventory >= 0
    assert 0 <= future.market_share <= 1

def test_generate_sample() -> None:
    generator = SyntheticDataGenerator(seed=42)

    sample = generator.generate_sample()

    assert sample.features.revenue > 0
    assert sample.features.demand_index > 0
    assert sample.target.horizon == 1
    assert sample.target.revenue > 0
    assert sample.target.profit != sample.features.profit

def test_generate_dataset() -> None:
    generator = SyntheticDataGenerator(seed=42)

    dataset = generator.generate_dataset(num_samples=100)

    assert len(dataset) == 100
    assert all(sample.target.horizon == 1 for sample in dataset)
    assert all(sample.features.revenue > 0 for sample in dataset)


def test_generate_dataset_rejects_invalid_size() -> None:
    generator = SyntheticDataGenerator(seed=42)

    try:
        generator.generate_dataset(num_samples=0)
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "num_samples must be greater than zero"

def test_generated_dataset_has_variation() -> None:
    generator = SyntheticDataGenerator(seed=42)

    dataset = generator.generate_dataset(num_samples=100)

    revenues = {sample.features.revenue for sample in dataset}
    demands = {sample.features.demand_index for sample in dataset}
    target_revenues = {sample.target.revenue for sample in dataset}

    assert len(revenues) > 1
    assert len(demands) > 1
    assert len(target_revenues) > 1