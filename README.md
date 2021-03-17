# DEX and AMM Add/Remove Contracts
Liquidity Exchange and Add to any listed Pool with XXX/ETH from any ERC20 token and develped in Vyper.

## Current Contracts deployed at:
1. Uniswap Liquidity:
  * Add: [0xFd8A61F94604aeD5977B31930b48f1a94ff3a195](https://etherscan.io/address/0xFd8A61F94604aeD5977B31930b48f1a94ff3a195)

  * Remove: [0x418915329226AE7fCcB20A2354BbbF0F6c22Bd92](https://etherscan.io/address/0x418915329226AE7fCcB20A2354BbbF0F6c22Bd92)


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
Run ganache-cli mainnet fork

```bash
ganache-cli --fork https://mainnet.infura.io/v3/#{YOUR_INFURA_KEY} -p 7545 -e 10000
```

Run brownie test

```bash
brownie test -s
```

## Deployment
```bash
brownie run deploy_uni_add.py --network mainnet # UniswapExchangeAdd
brownie run deploy_uni_remove.py --network mainnet # UniswapExchangeRemove
```

## Fees
This contract charges a flat, developer maintenance, transaction fee of 0.005ETH for any transaction greater than $5,000 USDC in value to help maintain and provide support for the contract and further improvements.