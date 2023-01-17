import pytest
from datetime import date
from airflow.providers.mnb.operators.mnb import MnbExchangeRateOperator
from airflow.exceptions import AirflowFailException

def test_rate_exists():
    expected = '{"date": "2023-01-16", "rates": [{"currency": "AUD", "rate": 256.81}, {"currency": "BGN", "rate": 203.99}, {"currency": "BRL", "rate": 72.36}, {"currency": "CAD", "rate": 275.26}, {"currency": "CHF", "rate": 398.61}, {"currency": "CNY", "rate": 54.8}, {"currency": "CZK", "rate": 16.62}, {"currency": "DKK", "rate": 53.63}, {"currency": "EUR", "rate": 398.98}, {"currency": "GBP", "rate": 449.86}, {"currency": "HKD", "rate": 47.2}, {"currency": "IDR", "rate": 0.0245}, {"currency": "ILS", "rate": 107.78}, {"currency": "INR", "rate": 4.52}, {"currency": "ISK", "rate": 2.59}, {"currency": "JPY", "rate": 2.872}, {"currency": "KRW", "rate": 0.2981}, {"currency": "MXN", "rate": 19.56}, {"currency": "MYR", "rate": 85.43}, {"currency": "NOK", "rate": 37.25}, {"currency": "NZD", "rate": 235.75}, {"currency": "PHP", "rate": 6.76}, {"currency": "PLN", "rate": 84.92}, {"currency": "RON", "rate": 80.69}, {"currency": "RSD", "rate": 3.4}, {"currency": "RUB", "rate": 5.39}, {"currency": "SEK", "rate": 35.4}, {"currency": "SGD", "rate": 279.24}, {"currency": "THB", "rate": 11.18}, {"currency": "TRY", "rate": 19.62}, {"currency": "UAH", "rate": 10.03}, {"currency": "USD", "rate": 368.71}, {"currency": "ZAR", "rate": 21.6}]}'
    operator = MnbExchangeRateOperator(task_id="test", date=date(2023,1,16))
    result = operator.execute({})
    assert result == expected

def test_rate_doesnt_exist():
    operator = MnbExchangeRateOperator(task_id="test", date=date(2023,1,15))
    with pytest.raises(AirflowFailException):
        operator.execute({})
    
