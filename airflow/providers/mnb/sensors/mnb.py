import datetime
from typing import Sequence

from airflow.sensors.base import BaseSensorOperator, PokeReturnValue
from airflow.utils.context import Context
from airflow.providers.mnb.hooks.mnb import MnbHook


class MnbExchangeRateSensor(BaseSensorOperator):
    template_fields: Sequence[str] = ("date",)

    def __init__(self, *, date: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.date = date
        self._hook = MnbHook()

    def poke(self, context: Context) -> bool | PokeReturnValue:
        self.log.info(f"Checking whether rates have been published for {self.date}")
        result = self._hook.has_rates(datetime.date.fromisoformat(self.date))
        self.log.info(f"Result: {result}")
        return result
