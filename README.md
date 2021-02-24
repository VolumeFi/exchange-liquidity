# DEX and AMM Add/Remove Contracts
Liquidity Exchange and Add to any listed Pool with XXX/ETH from any ERC20 token and develped in Vyper.

## Current Contracts deployed at:
1. Uniswap Liquidity Add:
  * [0xe327518a50651D536D189562641aF128aFbEcF48](https://etherscan.io/address/0xe327518a50651D536D189562641aF128aFbEcF48)

2. Curve Liquidity Add
* [PENDING]

## Infura Key
```bash
export WEB3_INFURA_PROJECT_ID=${YOUR_INFURA_KEY}
```

## Add account
```bash
brownie accounts new deployer_account
```

input private key and password


## Test
```bash
brownie test -s
```

## Deployment
```bash
brownie run deploy.py --network mainnet
```

## Fees
This contract charges a flat, developer maintenance, transaction fee of 0.005ETH for any transaction greater than $5,000 USDC in value to help maintain and provide support for the contract and further improvements.