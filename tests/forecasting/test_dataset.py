from abss.forecasting.dataset import ForecastDatasetBuilder
from abss.forecasting.synthetic_data import SyntheticDataGenerator


def test_features_to_vector() -> None:
    generator = SyntheticDataGenerator(seed=42)
    sample = generator.generate_sample()

    vector = ForecastDatasetBuilder.features_to_vector(sample)

    assert len(vector) == 18
    assert vector[0] == sample.features.revenue
    assert vector[1] == sample.features.profit
    assert vector[6] == sample.features.demand_index
    assert vector[17] == sample.features.cash_constraint_event


def test_target_to_vector() -> None:
    generator = SyntheticDataGenerator(seed=42)
    sample = generator.generate_sample()

    vector = ForecastDatasetBuilder.target_to_vector(sample)

    assert len(vector) == 5
    assert vector[0] == sample.target.revenue
    assert vector[1] == sample.target.profit
    assert vector[4] == sample.target.market_share

def test_build_dataset() -> None:
    generator = SyntheticDataGenerator(seed=42)
    samples = generator.generate_dataset(num_samples=10)

    builder = ForecastDatasetBuilder()

    features, targets = builder.build_dataset(samples)

    assert len(features) == 10
    assert len(targets) == 10
    assert all(len(row) == 18 for row in features)
    assert all(len(row) == 5 for row in targets)