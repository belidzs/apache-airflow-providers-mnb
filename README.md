# MNB Provider for Apache Airflow

This package contains all the necessary operators, hooks and sensors necessary to access the daily exchange rates published by MNB (Central Bank of Hungary) in Apache Airflow.

## Installation

You can install it with any package manager compatible with PyPI:

```
pip install apache-airflow-provider-mnb
```

## Components

| Component | Notes |
| - | - |
| `MnbHook` | Implements low-level functions to interact with MNB's API |
| `MnbExchangeRateOperator` | Provides access to the exchange rates published on a specific day |
| `MnbExchangeRateSensor` | Senses whether the rates were already published for a specific day

## Example
This following example demonstrates a typical use case:

1. Start running at 8:00AM every day
1. Check if the exchange rates were already published (repeat every 10 minutes)
1. Permanently fail after 3 hours if the rates were never published (there are no rates available on the weekends and public holidays)
1. Generate the SQL commands
1. Run them against a PostgreSQL database

```python
from datetime import date
import json
import pendulum
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.mnb.sensors.mnb import MnbExchangeRateSensor
from airflow.providers.mnb.operators.mnb import MnbExchangeRateOperator

@dag(
    dag_id="refresh_currency_rates",
    description="Refresh currency exchange rates",
    schedule="0 8 * * *",
    start_date=pendulum.datetime(2023, 1, 16, tz="Europe/Budapest"),
    catchup=False
)
def mnb():
    is_exchange_rate_available = MnbExchangeRateSensor(
        task_id="is_exchange_rate_available",
        timeout=10800,
        poke_interval=600,
        date="{{ ds }}"
    )
    
    exchange_rates = MnbExchangeRateOperator(
        task_id="get_exchange_rates",
        date="{{ ds }}"
    )
    
    @task
    def generate_queries(exchange_rates: str):
        rates = json.loads(exchange_rates)
        queries = ""
        mnb_date = rates["date"]
        for rate in rates["rates"]:
            currency_id = rate["currency"]
            mnb_rate = rate["rate"]
            queries += f"UPDATE finance.currency SET mnb_rate = '{mnb_rate}', mnb_date = '{mnb_date}' WHERE currency_id = '{currency_id}';\n"
        return queries

    is_exchange_rate_available >> exchange_rates

    queries = generate_queries(exchange_rates.output)
    PostgresOperator(
        task_id="update_exchange_rates",
        postgres_conn_id="postgres_default",
        database="erp",
        sql=queries)

mnb()
```