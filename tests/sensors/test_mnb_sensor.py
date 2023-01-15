from datetime import date
from airflow.providers.mnb.sensors.mnb import MnbExchangeRateSensor

def test_sensor_true():
    sensor = MnbExchangeRateSensor(task_id="test", date=date(2023,1,16))
    assert sensor.poke(context={}) == True


def test_sensor_false():
    sensor = MnbExchangeRateSensor(task_id="test", date=date(2023,1,15))
    assert sensor.poke(context={}) == False