# DEX and AMM Add/Remove Contracts
Liquidity Exchange and Add to any listed Pool with XXX/ETH from any ERC20 token and develped in Vyper.

## Current Contracts deployed at:
1. Uniswapv3 Liquidity:
  * Release1 Add: [0x8039722EE74dE2e37fDc39783b0a574Ea492DBAc](https://etherscan.io/address/0x8039722EE74dE2e37fDc39783b0a574Ea492DBAc)

 * Release1 Swapv2Addv3: [0xDA76A489b8148Ba6e409B04259CB14E75e5E9dd3](https://etherscan.io/address/0xDA76A489b8148Ba6e409B04259CB14E75e5E9dd3)

 * Release2 Swapv2Addv3: [0xE76427463FdBacdD0e794e5Ea30269f30Dd9B8eB](https://etherscan.io/address/0xE76427463FdBacdD0e794e5Ea30269f30Dd9B8eB)

2. Uniswapv2 Liquidity:
  * Release1 Add: [0xFd8A61F94604aeD5977B31930b48f1a94ff3a195](https://etherscan.io/address/0xFd8A61F94604aeD5977B31930b48f1a94ff3a195)

  * Release1 Remove: [0x418915329226AE7fCcB20A2354BbbF0F6c22Bd92](https://etherscan.io/address/0x418915329226AE7fCcB20A2354BbbF0F6c22Bd92)

  * Release2 Add: [0xA522AA47C40F2BAC847cbe4D37455c521E69DEa7](https://etherscan.io/address/0xA522AA47C40F2BAC847cbe4D37455c521E69DEa7)

  * Release2 Remove: [0x430f33353490b256D2fD7bBD9DaDF3BB7f905E78](https://etherscan.io/address/0x430f33353490b256D2fD7bBD9DaDF3BB7f905E78)


3. Curve Liquidity Add via Uniswap
  * Add: [0x6fC92B10f8f3b2247CbAbF5843F9499719b0653C](https://etherscan.io/address/0x6fC92B10f8f3b2247CbAbF5843F9499719b0653C)

  * Remove: [0xb833600aEbcC3FAb87d0116a8b1716f2a335bB95](https://etherscan.io/address/0xb833600aEbcC3FAb87d0116a8b1716f2a335bB95)


4. Sushiswap Liquidity Add via Sushiswap
  * Add: [0xe5826517134241278b6D372D1dA9f66D07190612](https://etherscan.io/address/0xe5826517134241278b6D372D1dA9f66D07190612)

  * Remove: [0x972b0Ff06c7c8e03468d841973cBB3578b6a7299](https://etherscan.io/address/0x972b0Ff06c7c8e03468d841973cBB3578b6a7299)


5. Balancer Liquidity Add via Balancer
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
```

Run brownie test

```bash
brownie test tests/test_00_main_uniswap.py -s
brownie test tests/test_01_main_sushiswap.py -s
brownie test tests/test_02_main_curve.py -s
brownie test tests/test_03_main_balancer.py -s
brownie test tests/test_04_main_uniswap_v3.py -s
```

## Deployment
```bash
brownie run deploy_uni_add.py --network mainnet # UniswapExchangeAdd
brownie run deploy_uni_remove.py --network mainnet # UniswapExchangeRemove
brownie run deploy_sushi_add.py --network mainnet # SushiSwapExchangeAdd
brownie run deploy_sushi_remove.py --network mainnet # SushiSwapExchangeRemove
brownie run deploy_curve_add.py --network mainnet # CurveExchangeAdd
brownie run deploy_curve_remove.py --network mainnet # CurveExchangeRemove
brownie run deploy_balancer_add.py --network mainnet # BalancerExchangeAdd
brownie run deploy_balancer_remove.py --network mainnet # BalancerExchangeRemove
brownie run deploy_univ3_add.py --network mainnet # UniswapV3ExchangeAdd
brownie run deploy_univ3_remove.py --network mainnet # UniswapV3ExchangeRemove
```

## Fees
This contract charges a flat, developer maintenance, transaction fee of 0.005ETH for any transaction greater than $5,000 USDC in value to help maintain and provide support for the contract and further improvements.