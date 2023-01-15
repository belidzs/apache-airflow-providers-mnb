import pytest
from airflow.providers.mnb.hooks.mnb import MnbHook
from datetime import date
from mnb import Mnb


@pytest.fixture
def hook():
    return MnbHook()

def test_init(hook: MnbHook):
    assert isinstance(hook, MnbHook)

def test_get_conn(hook: MnbHook):
    assert isinstance(hook.get_conn(), Mnb)

def test_has_rates_true(hook: MnbHook):
    assert hook.has_rates(date(2023,1,16))

def test_has_rates_false(hook: MnbHook):
    assert not hook.has_rates(date(2023,1,14))
