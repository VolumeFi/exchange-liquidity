# DEX and AMM Add/Remove Contracts
Liquidity Exchange and Add to any listed Pool with XXX/ETH from any ERC20 token and develped in Vyper.

## Current Contracts deployed at:
1. Uniswap Liquidity:
  * Release1 Add: [0xFd8A61F94604aeD5977B31930b48f1a94ff3a195](https://etherscan.io/address/0xFd8A61F94604aeD5977B31930b48f1a94ff3a195)

  * Release1 Remove: [0x418915329226AE7fCcB20A2354BbbF0F6c22Bd92](https://etherscan.io/address/0x418915329226AE7fCcB20A2354BbbF0F6c22Bd92)

  * Release2 Add: [0xA522AA47C40F2BAC847cbe4D37455c521E69DEa7](https://etherscan.io/address/0xA522AA47C40F2BAC847cbe4D37455c521E69DEa7)

  * Release2 Remove: [0x430f33353490b256D2fD7bBD9DaDF3BB7f905E78](https://etherscan.io/address/0x430f33353490b256D2fD7bBD9DaDF3BB7f905E78)


2. Curve Liquidity Add via Uniswap
  * Add: [0x6fC92B10f8f3b2247CbAbF5843F9499719b0653C](https://etherscan.io/address/0x6fC92B10f8f3b2247CbAbF5843F9499719b0653C)

  * Remove: [0xb833600aEbcC3FAb87d0116a8b1716f2a335bB95](https://etherscan.io/address/0xb833600aEbcC3FAb87d0116a8b1716f2a335bB95)


3. Sushiswap Liquidity Add via Sushiswap
  * Add: [0xe5826517134241278b6D372D1dA9f66D07190612](https://etherscan.io/address/0xe5826517134241278b6D372D1dA9f66D07190612)

  * Remove: [0x972b0Ff06c7c8e03468d841973cBB3578b6a7299](https://etherscan.io/address/0x972b0Ff06c7c8e03468d841973cBB3578b6a7299)


4. Balancer Liquidity Add via Balancer
  * Add: [0xe05b4871fDB9eAC749f4B809f600B74dF5B2b118](https://etherscan.io/address/0xe05b4871fDB9eAC749f4B809f600B74dF5B2b118)

  * Remove: [](https://etherscan.io/address/)


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
ganache-cli --fork https://rinkeby.infura.io/v3/#{YOUR_INFURA_KEY} -p 7545 -e 10000 # For UniswapV3 test, Other tests will be failed
```

Run brownie test

```bash
brownie test -s
brownie test tests/test_04_main_uniswap_v3.py -s # For UniswapV3 test on Rinkeby
```

## Deployment
```bash
brownie run deploy_uni_add.py --network mainnet # UniswapExchangeAdd
brownie run deploy_uni_remove.py --network mainnet # UniswapExchangeRemove
brownie run deploy_sushi_add.py --network mainnet # SushiSwapExchangeAdd
brownie run deploy_sushi_remove.py --network mainnet # SushiSwapExchangeRemove
brownie run deploy_univ3_add.py --network rinkeby # UniswapV3ExchangeAdd for Rinkeby
```

## Fees
This contract charges a flat, developer maintenance, transaction fee of 0.005ETH for any transaction greater than $5,000 USDC in value to help maintain and provide support for the contract and further improvements.