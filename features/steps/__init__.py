import os
import requests


NODE_ID = os.environ.get("NODE_ID")
if not NODE_ID:
    raise Exception('NODE_ID not set')

NODE_SIGNATURE = os.environ.get("NODE_SIGNATURE")
if not NODE_SIGNATURE:
    raise Exception('NODE_SIGNATURE not set')

KEY_IDENTIFIER = os.environ.get("KEY_IDENTIFIER")
if not KEY_IDENTIFIER:
    raise Exception('KEY_IDENTIFIER not set')

FULL_ADDRESS = os.environ.get("FULL_ADDRESS")
if not FULL_ADDRESS:
    raise Exception('FULL_ADDRESS not set')


def _get_base_url():
    return f'https://localhost:5500/api/{NODE_ID}/{NODE_SIGNATURE}'


def _get_private_key(address):
    full_url = f'{_get_base_url()}/PKUv2JfV87KpEZwE'

    resp = requests.get(full_url, params={'p0': address}, verify=False)

    return resp.json()["private_key_hex"]