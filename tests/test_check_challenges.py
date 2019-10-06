from hashlib import (
    sha256,
)
from random import (
    randint,
)

import pytest

import eth_utils

from .challenges import challenges


@pytest.mark.parametrize(
    'challenge_no,challenge', challenges.items()
)
def test_check_challenge(legendre_bounty_contract,
                         w3,
                         challenge_no,
                         challenge):
    call = legendre_bounty_contract.functions.challenges__redeemed(challenge_no)
    redeemed = call.call()
    assert not redeemed
    call = legendre_bounty_contract.functions.challenges__bounty(challenge_no)
    bounty = call.call()
    assert bounty == challenge["bounty"]
    call = legendre_bounty_contract.functions.challenges__check_length(challenge_no)
    check_length = call.call()
    assert check_length == challenge["check_length"]    
    call = legendre_bounty_contract.functions.challenges__check_value(challenge_no)
    check_value = call.call()
    assert check_value == challenge["check_value"]
    call = legendre_bounty_contract.functions.challenges__prime(challenge_no)
    prime = call.call()
    assert prime == challenge["prime"]


def test_challenges_length(legendre_bounty_contract,
                           w3):
    call = legendre_bounty_contract.functions.challenges_length()
    num = call.call()
    assert num == len(challenges)
