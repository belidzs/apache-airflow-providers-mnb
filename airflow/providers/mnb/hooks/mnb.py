from datetime import date
from typing import List
from mnb import Mnb
from mnb.models import Day

from airflow.hooks.base import BaseHook


class MnbHook(BaseHook):
    def __init__(self, context=None):
        super().__init__(context)
        self._client = None
    
    def get_conn(self) -> Mnb:
        if self._client is None:
            self._client = Mnb()
        return self._client

    def get_last_update(self) -> date:
        return self.get_conn().get_date_interval()[1]
    
    def has_rates(self, date: date) -> bool:
        result = self.get_conn().get_exchange_rates(date, date, ["EUR"])
        return len(result) == 1

    def get_exchange_rates(self, date: date) -> List[Day]:
        currencies = self.get_conn().get_currencies()
        return self.get_conn().get_exchange_rates(date, date, currencies)
