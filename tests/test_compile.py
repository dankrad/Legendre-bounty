from contract.utils import (
    get_legendre_bounty_bytecode,
)
from vyper import (
    compiler,
)


def test_compile_legendre_bounty_contract():
    legendre_bounty_contract_code = get_legendre_bounty_bytecode()
