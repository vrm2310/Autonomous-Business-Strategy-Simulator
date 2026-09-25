from abss.core.models import ForecastFeatures, ForecastTrainingSample


class ForecastDatasetBuilder:
    @staticmethod
    def features_to_vector(
        sample: ForecastTrainingSample,
    ) -> list[float]:
        return ForecastDatasetBuilder.features_to_vector_from_features(
            sample.features,
        )

    @staticmethod
    def target_to_vector(
        sample: ForecastTrainingSample,
    ) -> list[float]:
        target = sample.target

        return [
            target.revenue,
            target.profit,
            target.cash,
            target.inventory,
            target.market_share,
        ]

    @staticmethod
    def build_dataset(
        samples: list[ForecastTrainingSample],
    ) -> tuple[list[list[float]], list[list[float]]]:
        features = [
            ForecastDatasetBuilder.features_to_vector(sample)
            for sample in samples
        ]

        targets = [
            ForecastDatasetBuilder.target_to_vector(sample)
            for sample in samples
        ]

        return features, targets

    @staticmethod
    def features_to_vector_from_features(
        features: ForecastFeatures,
    ) -> list[float]:
        return [
            features.revenue,
            features.profit,
            features.cash,
            features.inventory,
            features.employees,
            features.market_share,
            features.demand_index,
            features.inflation_rate,
            features.interest_rate,
            features.competitor_pressure,
            features.seasonality_index,
            features.event_count,
            features.total_event_severity,
            features.high_inflation_event,
            features.high_competition_event,
            features.low_demand_event,
            features.demand_surge_event,
            features.cash_constraint_event,
        ]