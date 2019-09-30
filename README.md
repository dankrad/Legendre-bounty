# Legendre bounty smart contract

Explores the Legendre computation used in eth2.0 phase 1 proof-of-custody game as a smart contract.

The contract provides an interface to redeem a bounty that was set for Legendre key recovery (redeem_bounty method). In order to redeem a bounty, it first has to be locked by providing a sha256 hash of the key (this is to prevent front running once someone has found a valid solution).

# Requirements

This project uses `pipenv`, [https://docs.pipenv.org/en/latest/](https://docs.pipenv.org/en/latest/).

## Install

```bash
pipenv shell
pipenv install
```

## Compile

```bash
vyper contract/legendre_bit.vy
```

## Run tests

```bash
make test_install
make test
```