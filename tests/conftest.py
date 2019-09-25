from random import (
    randint,
)
import re

import pytest

from contract.utils import (
    get_legendre_bit_contract_code,
)
import eth_tester
from eth_tester import (
    EthereumTester,
    PyEVMBackend,
)
from vyper import (
    compiler,
)
from web3 import Web3
from web3.providers.eth_tester import (
    EthereumTesterProvider,
)

@pytest.fixture
def tester():
    return EthereumTester(PyEVMBackend())


@pytest.fixture
def a0(tester):
    return tester.get_accounts()[0]


@pytest.fixture
def w3(tester):
    web3 = Web3(EthereumTesterProvider(tester))
    return web3


@pytest.fixture
def legendre_bit_contract(w3, tester):
    legendre_bit_contract_code = get_legendre_bit_contract_code()
    contract_abi = compiler.mk_full_signature(legendre_bit_contract_code)
    contract_bytecode = compiler.compile_code(legendre_bit_contract_code)['bytecode']
    registration = w3.eth.contract(
        abi=contract_abi,
        bytecode=contract_bytecode)
    tx_hash = registration.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    registration_deployed = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=contract_abi
    )
    return registration_deployed


@pytest.fixture
def assert_tx_failed(tester):
    def assert_tx_failed(function_to_test, exception=eth_tester.exceptions.TransactionFailed):
        snapshot_id = tester.take_snapshot()
        with pytest.raises(exception):
            function_to_test()
        tester.revert_to_snapshot(snapshot_id)
    return assert_tx_failed
