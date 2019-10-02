from hashlib import (
    sha256,
)
from random import (
    randint,
)

import pytest

import eth_utils

from .utils import (
    jacobi_bit_multi
)
from .challenges import challenges

LOOP_ROUNDS = 2**32
HOUR = 3600
DAY = 24 * HOUR
YEAR = 365 * DAY
CONTRACT_VALIDITY = 3 * YEAR


def test_terminate(legendre_bounty_contract,
                   a0,
                   w3,
                   tester):
    pre_contract_balance = w3.eth.getBalance(legendre_bounty_contract.address)
    pre_balance = w3.eth.getBalance(a0)

    timestamp = w3.eth.getBlock('latest')['timestamp']
    tester.time_travel(timestamp + CONTRACT_VALIDITY)
    tester.mine_block()
    tester.mine_block()

    terminate_call = legendre_bounty_contract.functions.terminate_contract()
    tc_tx_hash = terminate_call.transact()
    tc_tx_receipt = w3.eth.waitForTransactionReceipt(tc_tx_hash)

    post_contract_balance = w3.eth.getBalance(legendre_bounty_contract.address)
    post_balance = w3.eth.getBalance(a0)
    assert post_contract_balance == 0
    assert post_balance - pre_balance > 0


def test_terminate_early(legendre_bounty_contract,
                         a0,
                         w3,
                         assert_tx_failed,
                         tester):

    timestamp = w3.eth.getBlock('latest')['timestamp']
    tester.time_travel(timestamp + CONTRACT_VALIDITY - 1000)
    tester.mine_block()
    tester.mine_block()

    terminate_call = legendre_bounty_contract.functions.terminate_contract()
    assert_tx_failed(terminate_call.transact)
