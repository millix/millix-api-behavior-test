from behave import *
import requests
import json
import time

from features.steps import _get_base_url, _get_private_key, NODE_ID, NODE_SIGNATURE, KEY_IDENTIFIER, FULL_ADDRESS


@given('we have a node running locally')
def step_impl(context):
    full_url = f'{_get_base_url()}/ZFAYRM8LRtmfYp4Y'

    resp = requests.get(full_url, verify=False)

    if resp.json()['node_id'] != NODE_ID:
        raise Exception("Invalid node id")


@given('we query the balance of {address}')
def step_impl(context, address):
    context.balance = _get_balance(address)

@given('we have a balance of atleast {amount} millix')
def step_impl(context, amount):
    outputs = _get_unspend_transaction_outputs(KEY_IDENTIFIER)

    total_balance = 0

    for transaction_output in outputs:
        total_balance += transaction_output["amount"]

    if total_balance < int(amount):
        raise Exception(f'Insufficient balance. Balance: {total_balance}. Needed: {amount}')

    context.current_balance = total_balance


@when('we query the private key')
def step_impl(context):
    context.response = _get_private_key(FULL_ADDRESS)


@when('we implement a test')
def step_impl(context):
    assert True is not False

@when('we query balance of {address}')
def step_impl(context, address):
    context.balance = _get_balance(address)


@when('we wait {amount} seconds')
def step_impl(context, amount):
    time.sleep(int(amount))


@then('behave will test it for us!')
def step_impl(context):
    assert True

@then('we should have a private key in the response')
def step_impl(context):
    assert context.response != ""


@then('we should have a balance larger than 0 in the response')
def step_impl(context):
    assert context.balance > 0

@then('we should have {amount} millix less when we query')
def step_impl(context, amount):
    new_balance = _get_balance(FULL_ADDRESS)

    print(f'Current balance: {context.current_balance}\n\nof')
    print(f'New balance {new_balance}')

    if context.current_balance - new_balance != int(amount):
        raise Exception(f'New balance: {new_balance}. Expected {context.current_balance - new_balance}')



def _get_balance(address):
    full_url = f'{_get_base_url()}/zLsiAkocn90e3K6R'

    resp = requests.get(full_url, params={'p0': address}, verify=False)

    return resp.json()['stable']

def _get_unspend_transaction_outputs(address_key_identifier):
    full_url = f'{_get_base_url()}/FDLyQ5uo5t7jltiQ'

    resp = requests.get(full_url, params={'p3': address_key_identifier, 'p10': '0', 'p7': '1'}, verify=False)

    return resp.json()
