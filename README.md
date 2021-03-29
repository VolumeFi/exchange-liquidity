# DEX and AMM Add/Remove Contracts
Liquidity Exchange and Add to any listed Pool with XXX/ETH from any ERC20 token and develped in Vyper.

## Current Contracts deployed at:
1. Uniswap Liquidity:
  * V1 Add: [0xFd8A61F94604aeD5977B31930b48f1a94ff3a195](https://etherscan.io/address/0xFd8A61F94604aeD5977B31930b48f1a94ff3a195)

  * V1 Remove: [0x418915329226AE7fCcB20A2354BbbF0F6c22Bd92](https://etherscan.io/address/0x418915329226AE7fCcB20A2354BbbF0F6c22Bd92)

  * V2 Add: [0xA522AA47C40F2BAC847cbe4D37455c521E69DEa7](https://etherscan.io/address/0xA522AA47C40F2BAC847cbe4D37455c521E69DEa7)

  * V2 Remove: [0xaa3E6Cd3eFabA178fF1eF87c03F85d8d48553572](https://etherscan.io/address/0xaa3E6Cd3eFabA178fF1eF87c03F85d8d48553572)


2. Curve Liquidity Add via Uniswap
  * Add: [0x6fC92B10f8f3b2247CbAbF5843F9499719b0653C](https://etherscan.io/address/0x6fC92B10f8f3b2247CbAbF5843F9499719b0653C)

  * Remove: [0xb833600aEbcC3FAb87d0116a8b1716f2a335bB95](https://etherscan.io/address/0xb833600aEbcC3FAb87d0116a8b1716f2a335bB95)


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