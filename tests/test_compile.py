from contract.utils import (
    get_legendre_bounty_contract_code,
)
from vyper import (
    compiler,
)


def test_compile_legendre_bounty_contract():
    legendre_bounty_contract_code = get_legendre_bounty_contract_code()
    abi = compiler.mk_full_signature(legendre_bounty_contract_code)
    bytecode = compiler.compile_code(legendre_bounty_contract_code)['bytecode']
