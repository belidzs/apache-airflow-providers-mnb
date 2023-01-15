from datetime import date

from airflow.sensors.base import BaseSensorOperator, PokeReturnValue
from airflow.utils.context import Context
from airflow.providers.mnb.hooks.mnb import MnbHook


class MnbExchangeRateSensor(BaseSensorOperator):
    def __init__(self, *, date: date, **kwargs) -> None:
        super().__init__(**kwargs)
        self._date = date
        self._hook = MnbHook()

    def poke(self, context: Context) -> bool | PokeReturnValue:
        self.log.info(f"Checking whether rates have been published for {self._date}")
        result = self._hook.has_rates(self._date)
        self.log.info(f"Result: {result}")
        return result
