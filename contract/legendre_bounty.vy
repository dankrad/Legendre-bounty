struct Challenge:
    check_value: uint256
    check_length: uint256
    prime: uint256
    bounty: wei_value
    redeemed: bool

LEGENDRE_BIT_MULTI_MAX: constant(uint256) = 256
HOUR: constant(timedelta) = 3600
DAY: constant(timedelta) = 24 * HOUR
YEAR: constant(timedelta) = 365 * DAY
CLAIM_DELAY: constant(timedelta) = 1 * DAY

owner: address 

challenges: public(map(uint256, Challenge))
challenges_length: public(uint256)

claims: public(map(bytes32, timestamp))


@public
@payable
def __init__():
    self.owner = msg.sender
    # Test challenges
    self.challenges[0] = Challenge({check_value: convert(0x0000000000000000000000000000000005d3446a44efe462f105619a1523928f, uint256),
                        check_length: 128,
                        prime: convert(0x000000000000000000000000000000000000000000000000ffffffffffffffc5, uint256),
                        bounty: 1000000000000000000,
                        redeemed: False})
    self.challenges[1] = Challenge({check_value: convert(0x000000000000000000000000000ccabbdd1a2ce2c7fba2177a60f26e4da3dfe4, uint256),
                        check_length: 148,
                        prime: convert(0x0000000000000000000000000000000000000000000003ffffffffffffffffdd, uint256),
                        bounty: 2000000000000000000,
                        redeemed: False})
    self.challenges[2] = Challenge({check_value: convert(0x000000000000000000000000000665172ef496d21b642f9762a741d65e1acb7e, uint256),
                        check_length: 148,
                        prime: convert(0x0000000000000000000000000000000000000000000fffffffffffffffffffdd, uint256),
                        bounty: 4000000000000000000,
                        redeemed: False})
    self.challenges[3] = Challenge({check_value: convert(0x0000000000000000000000000006f18b295f9e4d35025473b589dc1b0b5e10c7, uint256),
                        check_length: 148,
                        prime: convert(0x000000000000000000000000000000000000000ffffffffffffffffffffffff1, uint256),
                        bounty: 8000000000000000000,
                        redeemed: False})
    self.challenges[4] = Challenge({check_value: convert(0x000000000000000000000000000702d2c3f5a88d34d7ac4ca0d4792c15cbeead, uint256),
                        check_length: 148,
                        prime: convert(0x000000000000000000000000000fffffffffffffffffffffffffffffffffff59, uint256),
                        bounty: 16000000000000000000,
                        redeemed: False})
    self.challenges_length = 5


@private
def legendre_bit(input_a: uint256, q: uint256) -> uint256:
    a: uint256 = input_a
    if a >= q:
        a = a % q
    if a == 0:
        return 1

    assert(q > a and bitwise_and(q, 1) == 1)

    e: uint256 = (q - 1) / 2
    b: uint256 = 32

    # Call expmod precompile
    c: uint256 = convert(raw_call(0x0000000000000000000000000000000000000005, 
                         concat(convert(b, bytes32), # Base length
                                convert(b, bytes32), # Exponent length
                                convert(b, bytes32), # Modulus length
                                convert(a, bytes32), # Base
                                convert(e, bytes32), # Exponent
                                convert(q, bytes32)  # Modulus
    ), gas=100000, outsize=32), uint256)

    if c == q - 1:
        return 0
    return 1


@private
def legendre_bit_multi(input_a: uint256, q: uint256, input_n: uint256) -> uint256:
    a: uint256 = input_a
    r: uint256 = 0
    n: uint256 = input_n
    assert input_n < LEGENDRE_BIT_MULTI_MAX
    for i in range(LEGENDRE_BIT_MULTI_MAX):
        r = shift(r, 1)
        r = bitwise_or(r, self.legendre_bit(a, q))
        a += 1
        n -= 1
        if n == 0:
            break
    return r


@public
def legendre_bit_multi_test(input_a: uint256, q: uint256, input_n: uint256) -> uint256:
    return self.legendre_bit_multi(input_a, q, input_n)


@public
def claim_bounty(claim_hash: bytes32):
    assert self.claims[claim_hash] == 0
    self.claims[claim_hash] = block.timestamp + CLAIM_DELAY


@public
def redeem_bounty(challenge_no: uint256, key: uint256):
    assert challenge_no < self.challenges_length
    challenge: Challenge = self.challenges[challenge_no]
    assert not self.challenges[challenge_no].redeemed

    claim_hash: bytes32 = sha256(concat(convert(key, bytes32), convert(msg.sender, bytes32))) #, convert(msg.sender, bytes32)
    assert self.claims[claim_hash] > 0
    assert self.claims[claim_hash] < block.timestamp

    check_value: uint256 = self.legendre_bit_multi(key, self.challenges[challenge_no].prime, self.challenges[challenge_no].check_length)
    assert check_value == self.challenges[challenge_no].check_value
    self.challenges[challenge_no].redeemed = True
    send(msg.sender, challenge.bounty)


@public
def terminate_contract():
    assert msg.sender == self.owner
    selfdestruct(self.owner)
