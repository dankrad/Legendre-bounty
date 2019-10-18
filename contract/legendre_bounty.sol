pragma solidity ^0.5.11;

contract LegendreBounty {

    struct Challenge {
        uint check_value;
        uint check_length;
        uint prime;
        uint bounty;
        bool redeemed;
    }

    uint constant LEGENDRE_BIT_MULTI_MAX = 256;
    uint constant HOUR = 3600;
    uint constant DAY = 24 * HOUR;
    uint constant CLAIM_DELAY = 1 * DAY;

    address owner;

    mapping(uint => Challenge) public challenges;
    uint public challenges_length;

    mapping(bytes32 => uint256) public claims;


    constructor () public payable {
        owner = msg.sender;
        // Test challenges
        challenges[0] = Challenge({check_value: 0x0000000000000000000000000000000005d3446a44efe462f105619a1523928f,
                            check_length: 128,
                            prime: 0x000000000000000000000000000000000000000000000000ffffffffffffffc5,
                            bounty: 1000000000000000000,
                            redeemed: false});
        challenges[1] = Challenge({check_value: 0x000000000000000000000000000ccabbdd1a2ce2c7fba2177a60f26e4da3dfe4,
                            check_length: 148,
                            prime: 0x0000000000000000000000000000000000000000000003ffffffffffffffffdd,
                            bounty: 2000000000000000000,
                            redeemed: false});
        challenges[2] = Challenge({check_value: 0x000000000000000000000000000665172ef496d21b642f9762a741d65e1acb7e,
                            check_length: 148,
                            prime: 0x0000000000000000000000000000000000000000000fffffffffffffffffffdd,
                            bounty: 4000000000000000000,
                            redeemed: false});
        challenges[3] = Challenge({check_value: 0x0000000000000000000000000006f18b295f9e4d35025473b589dc1b0b5e10c7,
                            check_length: 148,
                            prime: 0x000000000000000000000000000000000000000ffffffffffffffffffffffff1,
                            bounty: 8000000000000000000,
                            redeemed: false});
        challenges[4] = Challenge({check_value: 0x000000000000000000000000000702d2c3f5a88d34d7ac4ca0d4792c15cbeead,
                            check_length: 148,
                            prime: 0x000000000000000000000000000fffffffffffffffffffffffffffffffffff59,
                            bounty: 16000000000000000000,
                            redeemed: false});
        challenges_length = 5;
    }


    function expmod(uint base, uint e, uint m) private view returns (uint o) {
        assembly {
            // define pointer
            let p := mload(0x40)
            // store data assembly-favouring ways
            mstore(p, 0x20)             // Length of Base
            mstore(add(p, 0x20), 0x20)  // Length of Exponent
            mstore(add(p, 0x40), 0x20)  // Length of Modulus
            mstore(add(p, 0x60), base)  // Base
            mstore(add(p, 0x80), e)     // Exponent
            mstore(add(p, 0xa0), m)     // Modulus
            if iszero(staticcall(sub(gas, 2000), 0x05, p, 0xc0, p, 0x20)) {
                revert(0, 0)
            }
            // data
            o := mload(p)
        }
    }
    
    
    function legendre_bit(uint input_a, uint q) private view returns (uint) {
        uint a = input_a;
        if(a >= q) {
            a = a % q;
        }
        if(a == 0) {
            return 1;
        }
    
        require(q > a && q & 1 == 1);
    
        uint e = (q - 1) / 2;
    
        // Call expmod precompile
        uint c = expmod(a, e, q);
    
        if(c == q - 1) {
            return 0;
        }
        return 1;
    }
    
    
    function legendre_bit_multi(uint input_a, uint q, uint n) public view returns (uint) {
        uint a = input_a;
        uint r = 0;
        require(n < LEGENDRE_BIT_MULTI_MAX);
        for(uint i = 0; i < n; i++) {
            r = r << 1;
            r = r ^ legendre_bit(a, q);
            a += 1;
        }
        return r;
    }
    
    
    function claim_bounty(bytes32 claim_hash) public {
        require(claims[claim_hash] == 0);
        claims[claim_hash] = block.timestamp + CLAIM_DELAY;
    }
    
    
    function redeem_bounty(uint challenge_no, uint key) public {
        require(challenge_no < challenges_length);
        require(!challenges[challenge_no].redeemed);
    
        bytes32 claim_hash = sha256(abi.encodePacked(bytes32(key), bytes32(uint256(msg.sender))));
        require(claims[claim_hash] > 0);
        require(claims[claim_hash] < block.timestamp);
    
        uint check_value = legendre_bit_multi(key, challenges[challenge_no].prime, challenges[challenge_no].check_length);
        require(check_value == challenges[challenge_no].check_value);
        challenges[challenge_no].redeemed = true;
        msg.sender.transfer(challenges[challenge_no].bounty);
    }
    
    
    function terminate_contract() public {
        require(msg.sender == owner);
        selfdestruct(msg.sender);
    }

}