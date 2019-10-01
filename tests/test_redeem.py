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

def jacobi_bit_mpz(a, n):
    return 1 if jacobi(a, n) >= 0 else 0

def jacobi_bit_multi(a, n, m):
    r = 0
    for i in range(m):
        r *= 2
        r += jacobi_bit_mpz(a + i, n)
    return r


@pytest.mark.parametrize(
    'challenge_no,challenge', challenges.items()
)
def test_redeem(legendre_bit_contract,
                      w3,
                      challenge_no,
                      challenge):
    pre_contract_balance = w3.eth.getBalance(legendre_bit_contract.address)
    pre_balance = w3.eth.getBalance(w3.eth.accounts[0])
    print(w3.eth.accounts[0])

    lock_call = legendre_bit_contract.functions.lock_bounty(sha256(challenge["key"].to_bytes(32, "big")
        + bytes.fromhex(w3.eth.accounts[0][2:]).rjust(32, b"\0")).digest())
    lock_call.transact()

    call = legendre_bit_contract.functions.redeem_bounty(challenge_no, challenge["key"])
    print(call.estimateGas())
    tx_hash = call.transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    post_contract_balance = w3.eth.getBalance(legendre_bit_contract.address)
    post_balance = w3.eth.getBalance(w3.eth.accounts[0])
    assert pre_contract_balance - post_contract_balance == challenge["bounty"]
    assert post_balance - pre_balance > 0


@pytest.mark.parametrize(
    'challenge_no,challenge', challenges.items()
)
def test_double_redeem(legendre_bit_contract,
                        w3,
                        assert_tx_failed,
                        challenge_no,
                        challenge):

    lock_call = legendre_bit_contract.functions.lock_bounty(sha256(challenge["key"].to_bytes(32, "big")
        + bytes.fromhex(w3.eth.accounts[0][2:]).rjust(32, b"\0")).digest())
    lock_call.transact()

    call = legendre_bit_contract.functions.redeem_bounty(challenge_no, challenge["key"])
    tx_hash = call.transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    assert_tx_failed(call.transact)


@pytest.mark.parametrize(
    'challenge_no,challenge', challenges.items()
)
def test_redeem_no_lock(legendre_bit_contract,
                        w3,
                        assert_tx_failed,
                        challenge_no,
                        challenge):

    call = legendre_bit_contract.functions.redeem_bounty(challenge_no, challenge["key"])
    
    assert_tx_failed(call.transact)


@pytest.mark.parametrize(
    'challenge_no,challenge', challenges.items()
)
def test_incorrect_redeem(legendre_bit_contract,
                        w3,
                        assert_tx_failed,
                        challenge_no,
                        challenge):

    lock_call = legendre_bit_contract.functions.lock_bounty(sha256((challenge["key"] + 1).to_bytes(32, "big")).digest())
    lock_call.transact()

    call = legendre_bit_contract.functions.redeem_bounty(challenge_no, challenge["key"] + 1)
    assert_tx_failed(call.transact)
