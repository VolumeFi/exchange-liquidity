# Uniswap Exchanage Add
Liquidity Exchange and Add to any Uniswap Pool XXX/ETH from any ERC20 token and develped in Vyper.

## Current Contract deployed at:
[0xFd8A61F94604aeD5977B31930b48f1a94ff3a195](https://etherscan.io/address/0xFd8A61F94604aeD5977B31930b48f1a94ff3a195)

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

# Fees
This contract charges a flat, developer maintenance, transaction fee of 0.005ETH for any transaction greater than $5,000 USDC in value to help maintain and provide support for the contract and further improvements.