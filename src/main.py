from AlgorithmImports import *

class StrategyLab(QCAlgorithm):
    """
    StrategyLab V1
    First working skeleton.
    """

    def initialize(self):
        self.set_start_date(2022, 1, 1)
        self.set_end_date(2025, 12, 31)
        self.set_cash(100000)

        self.set_brokerage_model(
            BrokerageName.INTERACTIVE_BROKERS_BROKERAGE,
            AccountType.MARGIN
        )

        self.universe_settings.resolution = Resolution.DAILY

        self.add_universe(self.coarse_selection)

        self.selected = []

    def coarse_selection(self, coarse):
        filtered = [
            c for c in coarse
            if c.has_fundamental_data
            and c.price > 10
            and c.dollar_volume > 50_000_000
        ]

        filtered = sorted(
            filtered,
            key=lambda x: x.dollar_volume,
            reverse=True
        )

        self.selected = [x.symbol for x in filtered[:200]]
        return self.selected

    def on_data(self, data: Slice):
        # V1 only scans and builds the investable universe.
        # Trading logic will be added in the next module.
        pass
