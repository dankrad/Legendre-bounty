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
    call = legendre_bounty_contract.functions.challenges(challenge_no)
    check_value, check_length, prime, bounty, redeemed = call.call()
    assert not redeemed
    assert bounty == challenge["bounty"]
    assert check_length == challenge["check_length"]    
    assert check_value == challenge["check_value"]
    assert prime == challenge["prime"]


def test_challenges_length(legendre_bounty_contract,
                           w3):
    call = legendre_bounty_contract.functions.challenges_length()
    num = call.call()
    assert num == len(challenges)
