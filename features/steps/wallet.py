from behave import *
import requests
from features.steps import _get_base_url


@when('we query the mnemonic')
def step_impl(context):
    context.response = _get_mnemonic()

@then('we should have mnemonic in the response')
def step_impl(context):
    assert len(context.response['mnemonic_phrase'].split(' ')) == 24

def _get_mnemonic():
    full_url = f'{_get_base_url()}/BPZZ0l2nTfMSmmpl'

    resp = requests.get(full_url, verify=False)

    return resp.json()

