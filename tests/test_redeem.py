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
LOCK_DELAY = 1 * DAY


@pytest.mark.parametrize(
    'challenge_no,challenge', challenges.items()
)
def test_redeem(legendre_bounty_contract,
                a0,
                w3,
                tester,
                challenge_no,
                challenge):
    pre_contract_balance = w3.eth.getBalance(legendre_bounty_contract.address)
    pre_balance = w3.eth.getBalance(a0)

    lock_call = legendre_bounty_contract.functions.lock_bounty(sha256(challenge["key"].to_bytes(32, "big")
        + bytes.fromhex(a0[2:]).rjust(32, b"\0")).digest())
    lc_tx_hash = lock_call.transact()
    lc_tx_receipt = w3.eth.waitForTransactionReceipt(lc_tx_hash)
    timestamp = w3.eth.getBlock('latest')['timestamp']
    tester.time_travel(timestamp + LOCK_DELAY)
    tester.mine_block()


    call = legendre_bounty_contract.functions.redeem_bounty(challenge_no, challenge["key"])
    print(call.estimateGas())
    
    tx_hash = call.transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    post_contract_balance = w3.eth.getBalance(legendre_bounty_contract.address)
    post_balance = w3.eth.getBalance(a0)
    assert pre_contract_balance - post_contract_balance == challenge["bounty"]
    assert post_balance - pre_balance > 0


@pytest.mark.parametrize(
    'challenge_no,challenge', challenges.items()
)
def test_double_redeem(legendre_bounty_contract,
                       a0,
                       w3,
                       tester,
                       assert_tx_failed,
                       challenge_no,
                       challenge):

    lock_call = legendre_bounty_contract.functions.lock_bounty(sha256(challenge["key"].to_bytes(32, "big")
        + bytes.fromhex(a0[2:]).rjust(32, b"\0")).digest())
    lc_tx_hash = lock_call.transact()
    lc_tx_receipt = w3.eth.waitForTransactionReceipt(lc_tx_hash)
    timestamp = w3.eth.getBlock('latest')['timestamp']
    tester.time_travel(timestamp + LOCK_DELAY)
    tester.mine_block()

    call = legendre_bounty_contract.functions.redeem_bounty(challenge_no, challenge["key"])
    tx_hash = call.transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    assert_tx_failed(call.transact)


@pytest.mark.parametrize(
    'challenge_no,challenge', challenges.items()
)
def test_early_redeem(legendre_bounty_contract,
                      a0,
                      w3,
                      tester,
                      assert_tx_failed,
                      challenge_no,
                      challenge):
    lock_call = legendre_bounty_contract.functions.lock_bounty(sha256(challenge["key"].to_bytes(32, "big")
        + bytes.fromhex(a0[2:]).rjust(32, b"\0")).digest())
    lc_tx_hash = lock_call.transact()
    lc_tx_receipt = w3.eth.waitForTransactionReceipt(lc_tx_hash)
    timestamp = w3.eth.getBlock('latest')['timestamp']
    tester.time_travel(timestamp + LOCK_DELAY - 1000)
    tester.mine_block()
    tester.mine_block()

    call = legendre_bounty_contract.functions.redeem_bounty(challenge_no, challenge["key"])
    
    assert_tx_failed(call.transact)


@pytest.mark.parametrize(
    'challenge_no,challenge', challenges.items()
)
def test_redeem_no_lock(legendre_bounty_contract,
                        w3,
                        assert_tx_failed,
                        challenge_no,
                        challenge):

    call = legendre_bounty_contract.functions.redeem_bounty(challenge_no, challenge["key"])
    
    assert_tx_failed(call.transact)


@pytest.mark.parametrize(
    'challenge_no,challenge', challenges.items()
)
def test_incorrect_redeem(legendre_bounty_contract,
                          w3,
                          assert_tx_failed,
                          challenge_no,
                          challenge):

    lock_call = legendre_bounty_contract.functions.lock_bounty(sha256((challenge["key"] + 1).to_bytes(32, "big")).digest())
    lock_call.transact()

    call = legendre_bounty_contract.functions.redeem_bounty(challenge_no, challenge["key"] + 1)
    assert_tx_failed(call.transact)


def test_double_lock(legendre_bounty_contract,
                       a0,
                       w3,
                       tester,
                       assert_tx_failed):

    lock_call = legendre_bounty_contract.functions.lock_bounty(sha256((0).to_bytes(32, "big")
        + bytes.fromhex(a0[2:]).rjust(32, b"\0")).digest())
    lc_tx_hash = lock_call.transact()
    lc_tx_receipt = w3.eth.waitForTransactionReceipt(lc_tx_hash)

    assert_tx_failed(lock_call.transact)
