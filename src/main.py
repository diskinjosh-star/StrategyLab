from AlgorithmImports import *

from config import (
    END_DATE,
    MIN_DOLLAR_VOLUME,
    MIN_PRICE,
    START_DATE,
    STARTING_CASH,
    UNIVERSE_REFRESH,
    UNIVERSE_SIZE,
)


class StrategyLab(QCAlgorithm):
    """
    StrategyLab V1: liquid US-equity universe scanner.

    This version intentionally does not trade. It verifies that the
    point-in-time universe and Interactive Brokers reality model work
    before we add Anchored VWAP signals and order management.
    """

    def initialize(self) -> None:
        self.set_start_date(*START_DATE)
        self.set_end_date(*END_DATE)
        self.set_cash(STARTING_CASH)

        self.set_brokerage_model(
            BrokerageName.INTERACTIVE_BROKERS_BROKERAGE,
            AccountType.MARGIN,
        )

        self.universe_settings.resolution = Resolution.DAILY
        self.universe_settings.asynchronous = True

        if UNIVERSE_REFRESH == "monthly":
            self.universe_settings.schedule.on(self.date_rules.month_start())

        self._selected_symbols = []
        self._active_symbols = set()

        self._universe = self.add_universe(self._select_fundamentals)

        self.set_runtime_statistic("Scanner", "Starting")
        self.debug("StrategyLab V1 initialized.")

    def _select_fundamentals(self, fundamentals):
        eligible = [
            item
            for item in fundamentals
            if item.has_fundamental_data
            and item.price >= MIN_PRICE
            and item.dollar_volume >= MIN_DOLLAR_VOLUME
        ]

        ranked = sorted(
            eligible,
            key=lambda item: item.dollar_volume,
            reverse=True,
        )

        self._selected_symbols = [
            item.symbol for item in ranked[:UNIVERSE_SIZE]
        ]

        self.set_runtime_statistic(
            "Scanner",
            f"{len(self._selected_symbols)} selected",
        )

        return self._selected_symbols

    def on_securities_changed(self, changes: SecurityChanges) -> None:
        for security in changes.added_securities:
            self._active_symbols.add(security.symbol)

        for security in changes.removed_securities:
            self._active_symbols.discard(security.symbol)

        self.set_runtime_statistic(
            "Active Universe",
            str(len(self._active_symbols)),
        )

        if changes.added_securities or changes.removed_securities:
            self.debug(
                f"{self.time.date()}: "
                f"added={len(changes.added_securities)}, "
                f"removed={len(changes.removed_securities)}, "
                f"active={len(self._active_symbols)}"
            )

    def on_data(self, data: Slice) -> None:
        pass
