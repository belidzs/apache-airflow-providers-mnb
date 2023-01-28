from datetime import date 
from typing import Optional, Sequence
from functools import cached_property
from airflow.providers.mnb.hooks.mnb import MnbHook
from airflow.utils.context import Context
from airflow.models.baseoperator import BaseOperator
from airflow.exceptions import AirflowFailException


class MnbExchangeRateOperator(BaseOperator):
    template_fields: Sequence[str] = ("date",)
    
    def __init__(self, *, date: str, **kwargs):
        super().__init__(**kwargs)
        self.date = date

    @cached_property
    def hook(self) -> MnbHook:
        return MnbHook()

    def execute(self, context: Context) -> Optional[str]:
        self.log.info(f"Getting exchange rates for {self.date}")
        days = self.hook.get_exchange_rates(date.fromisoformat(self.date))
        if len(days) == 0:
            raise AirflowFailException("Exchange rates have not been published for the provided date")
        self.log.info("Success")
        return days[0].to_json()
