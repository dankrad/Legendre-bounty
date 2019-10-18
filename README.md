# Legendre bounty smart contract

Explores the Legendre computation used in eth2.0 phase 1 proof-of-custody game as a smart contract.

The contract provides an interface to redeem a bounty that was set for Legendre key recovery (redeem_bounty method). In order to redeem a bounty, it first has to be locked by providing a sha256 hash of the key (this is to prevent front running once someone has found a valid solution).

# Requirements

This project uses `pipenv`, https://docs.pipenv.org/en/latest/.

## Installation

### Prerequisites

On MacOS:

```bash
brew install gmp libmpc mpfr
```

## To install package

```bash
pipenv shell
pipenv install
```

## Compile

```bash
vyper contract/legendre_bounty.vy
```

## Run tests

```bash
make test_install
make test
```

## Run with gas cost estimates

To enable debug printing, run pytest with extra flags:

```bash
pipenv run pytest -s -v -k test_legendre_bit_multi
```
