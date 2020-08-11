from behave import *
import requests
import time
import json

from features.steps import _get_base_url,  KEY_IDENTIFIER, _get_private_key


@when('we query transaction output of transaction {transaction_id} at position {position} in shard {shard_name}')
def step_impl(context, transaction_id, position, shard_name):
    context.response = _query_output(transaction_id, position, shard_name)

@then('we should have an output with {amount} millix in the response')
def step_impl(context, amount):
    assert context.response['amount'] == int(amount)

@when('we send {amount} millix to {address} {count} times with {sleep_time} seconds interval')
def step_impl(context, amount, address, count, sleep_time):
    for i in range(0, int(count)):
        _send_millix(int(amount), address)
        time.sleep(int(sleep_time))

@when('we send {amount} millix to {receiver_address}')
def step_impl(context, amount, receiver_address):
    _send_millix(amount, receiver_address)


def _query_output(tx_id, position, shard_name):
    full_url = f'{_get_base_url()}/KN2ZttYDEKzCulEZ'

    resp = requests.get(full_url, params={'p0': tx_id, 'p1': position, 'p2': shard_name}, verify=False)

    return resp.json()


def _send_millix(amount, receiver_address):
    outputs = _get_unspend_transaction_outputs(KEY_IDENTIFIER)

    chosen_amount = 0
    chosen_outputs = []

    addresses = set()

    for output in outputs:
        chosen_amount += output["amount"]

        addresses.add((output["address"], output['address_key_identifier']))
        chosen_outputs.append(output)

        if chosen_amount >= int(amount):
            break

    keys = {}

    for (address, key_identifier) in addresses:
        priv_key = _get_private_key(address)
        keys[key_identifier] = priv_key

    inputs = []

    for output in chosen_outputs:
        inputs.append({
            'address_base': output['address_key_identifier'],
            'address_key_identifier': output['address_key_identifier'],
            'address_version': 'lal',
            'output_position': output['output_position'],
            'output_shard_id': output['shard_id'],
            'output_transaction_date': output['transaction_date'],
            'output_transaction_id': output['transaction_id'],
        })

    output = {
        'address_base': receiver_address,
        'address_version': 'lal',
        'address_key_identifier': receiver_address,
        'amount': int(amount),
    }

    change_output = {
        'address_base': KEY_IDENTIFIER,
        'address_version': 'lal',
        'address_key_identifier': KEY_IDENTIFIER,
        'amount': chosen_amount - int(amount),
    }

    transaction = {
        'transaction_version': 'la0l',
        'transaction_output_list': [output, change_output],
        'transaction_input_list': inputs,
    }

    print(f'\nTransaction: {json.dumps(transaction)}\n')
    print(f'\nKey map: {json.dumps(keys)}\n')

    signed_transaction = _sign_transaction(transaction, keys)

    print(f'\nSigned transaction: {json.dumps(signed_transaction)}\n')

    _send_transaction(signed_transaction)


def _get_unspend_transaction_outputs(address_key_identifier):
    full_url = f'{_get_base_url()}/FDLyQ5uo5t7jltiQ'

    resp = requests.get(full_url, params={'p3': address_key_identifier, 'p10': '0', 'p7': '1'}, verify=False)

    return resp.json()



def _sign_transaction(payload, keymap):
    full_url = f'{_get_base_url()}/RVBqKlGdk9aEhi5J'

    resp = requests.get(full_url, params={'p0': json.dumps(payload),  'p1': json.dumps(keymap)}, verify=False)

    res = resp.json()
    if 'status' in res and res['status'] == 'fail':
        raise Exception(f'Error. Message: {res}')

    return res

def _send_transaction(signed_transaction):
    full_url = f'{_get_base_url()}/VnJIBrrM0KY3uQ9X'

    resp = requests.get(full_url, params={'p0': json.dumps(signed_transaction)}, verify=False)

    res = resp.json()

    print(res)

    status = res['status']

    if status != 'success':
        raise Exception(f'Error. Status: {status}')
