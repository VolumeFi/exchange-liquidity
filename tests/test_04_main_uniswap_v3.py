#!/usr/bin/python3

import pytest
import math

def test_main(USDC, DAI, WETH, accounts, UniswapV2Router02, MyUniswapV3ExchangeAdd, MyUniswapV3ExchangeRemove, Contract):
    MyNonfungiblePositionManager = Contract.from_abi("NonfungiblePositionManager", "0xC36442b4a4522E871399CD717aBDD847Ab11FE88", [{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH9","type":"address"},{"internalType":"address","name":"_tokenDescriptor_","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"approved","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":False,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":False,"internalType":"address","name":"recipient","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Collect","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":False,"internalType":"uint128","name":"liquidity","type":"uint128"},{"indexed":False,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"DecreaseLiquidity","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":False,"internalType":"uint128","name":"liquidity","type":"uint128"},{"indexed":False,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"IncreaseLiquidity","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WETH9","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint128","name":"amount0Max","type":"uint128"},{"internalType":"uint128","name":"amount1Max","type":"uint128"}],"name":"collect","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"}],"name":"createAndInitializePoolIfNecessary","outputs":[{"internalType":"address","name":"pool","type":"address"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"decreaseLiquidity","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"amount0Desired","type":"uint256"},{"internalType":"uint256","name":"amount1Desired","type":"uint256"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"increaseLiquidity","outputs":[{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint256","name":"amount0Desired","type":"uint256"},{"internalType":"uint256","name":"amount1Desired","type":"uint256"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"internalType":"structINonfungiblePositionManager.MintParams","name":"params","type":"tuple"}],"name":"mint","outputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"positions","outputs":[{"internalType":"uint96","name":"nonce","type":"uint96"},{"internalType":"address","name":"operator","type":"address"},{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"feeGrowthInside0LastX128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthInside1LastX128","type":"uint256"},{"internalType":"uint128","name":"tokensOwed0","type":"uint128"},{"internalType":"uint128","name":"tokensOwed1","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount0Owed","type":"uint256"},{"internalType":"uint256","name":"amount1Owed","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"uniswapV3MintCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"unwrapWETH9","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}])
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("USDC Balance")
    print(USDC.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))
    print(USDC.balanceOf(MyUniswapV3ExchangeAdd))
    UniswapV2Router02.swapETHForExactTokens(10000 * 10 ** 6, [WETH, USDC], accounts[0], 2 ** 256 - 1, {"from":accounts[0], "value": 10 * 10 ** 18})
    USDC.approve(MyUniswapV3ExchangeAdd, 10000 * 10 ** 6, {"from":accounts[0]})
    uniV3Params = [DAI, WETH, 3000, -210000, 210000, getSqrtRatioAtTick(-210000), getSqrtRatioAtTick(210000), 0, accounts[0], 2 ** 256 - 1]
    MyUniswapV3ExchangeAdd.investTokenForUniPair(USDC, 10000 * 10 ** 6, 0, uniV3Params, {"from":accounts[0], "value": 5 * 10 ** 15})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("USDC Balance")
    print(USDC.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))
    print(USDC.balanceOf(MyUniswapV3ExchangeAdd))
    WETH.deposit({"from": accounts[0], "value": 50 * 10 ** 18})
    UniswapV2Router02.swapETHForExactTokens(100000 * 10 ** 18, [WETH, DAI], accounts[0], 2 ** 256 - 1, {"from":accounts[0], "value": 100 * 10 ** 18})
    uniV3Params = [DAI, WETH, 500, -100000, 100000, 0xb8507a820728200000,  0xde0b6b3a7640000, 0, 0, accounts[0], 2 ** 256 - 1]
    WETH.approve(MyUniswapV3ExchangeAdd, 0xde0b6b3a7640000, {"from": accounts[0]})
    DAI.approve(MyUniswapV3ExchangeAdd, 0xb8507a820728200000, {"from": accounts[0]})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))
    print("-----STEP1-----")
    MyUniswapV3ExchangeAdd.addLiquidityForUniV3(0, uniV3Params, {'from': accounts[0]})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))
    token_id_1 = MyNonfungiblePositionManager.tokenOfOwnerByIndex(accounts[0], 0)
    WETH.approve(MyUniswapV3ExchangeAdd, 0xde0b6b3a7640000, {"from": accounts[0]})
    DAI.approve(MyUniswapV3ExchangeAdd, 0xb8507a820728200000, {"from": accounts[0]})
    
    print("-----STEP2-----")
    MyUniswapV3ExchangeAdd.addLiquidityForUniV3(token_id_1, uniV3Params, {'from': accounts[0]})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))
    uniV3Params = [DAI, WETH, 3000, -120000, 120000, 0xb8507a820728200000,  0xde0b6b3a7640000, 0, 0, accounts[0], 2 ** 256 - 1]
    WETH.approve(MyUniswapV3ExchangeAdd, 0xde0b6b3a7640000, {"from": accounts[0]})
    DAI.approve(MyUniswapV3ExchangeAdd, 0xb8507a820728200000, {"from": accounts[0]})
    
    print("-----STEP3-----")
    MyUniswapV3ExchangeAdd.addLiquidityForUniV3(0, uniV3Params, {'from': accounts[0]})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))
    token_id_2 = MyNonfungiblePositionManager.tokenOfOwnerByIndex(accounts[0], 1)
    WETH.approve(MyUniswapV3ExchangeAdd, 0xde0b6b3a7640000, {"from": accounts[0]})
    DAI.approve(MyUniswapV3ExchangeAdd, 0xb8507a820728200000, {"from": accounts[0]})
    
    print("-----STEP4-----")
    MyUniswapV3ExchangeAdd.addLiquidityForUniV3(token_id_2, uniV3Params, {'from': accounts[0]})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))
    
    uniV3Params = [DAI, WETH, 500, -100000, 100000, 0xb8507a820728200000,  0xde0b6b3a7640000, 0, 0, accounts[0], 2 ** 256 - 1]
    DAI.approve(MyUniswapV3ExchangeAdd, 0xb8507a820728200000, {"from": accounts[0]})
    print("-----STEP5-----")
    MyUniswapV3ExchangeAdd.addLiquidityEthForUniV3(0, uniV3Params, {'from': accounts[0], 'value': 0xde0b6b3a7640000})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))
    token_id_3 = MyNonfungiblePositionManager.tokenOfOwnerByIndex(accounts[0], 2)
    DAI.approve(MyUniswapV3ExchangeAdd, 0xb8507a820728200000, {"from": accounts[0]})
    
    print("-----STEP6-----")
    MyUniswapV3ExchangeAdd.addLiquidityEthForUniV3(token_id_3, uniV3Params, {'from': accounts[0], 'value': 0xde0b6b3a7640000})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))
    uniV3Params = [DAI, WETH, 3000, -120000, 120000, 0xb8507a820728200000,  0xde0b6b3a7640000, 0, 0, accounts[0], 2 ** 256 - 1]
    DAI.approve(MyUniswapV3ExchangeAdd, 0xb8507a820728200000, {"from": accounts[0]})

    print("-----STEP7-----")
    MyUniswapV3ExchangeAdd.addLiquidityEthForUniV3(0, uniV3Params, {'from': accounts[0], 'value': 0xde0b6b3a7640000})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))
    token_id_4 = MyNonfungiblePositionManager.tokenOfOwnerByIndex(accounts[0], 3)
    DAI.approve(MyUniswapV3ExchangeAdd, 0xb8507a820728200000, {"from": accounts[0]})

    print("-----STEP8-----")
    MyUniswapV3ExchangeAdd.addLiquidityEthForUniV3(token_id_4, uniV3Params, {'from': accounts[0], 'value': 0xde0b6b3a7640000})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))

    modifyParams = [500, -100000, -50000, accounts[0], 2 ** 256 - 1]
    print("-----STEP9-----")
    MyNonfungiblePositionManager.approve(MyUniswapV3ExchangeAdd, token_id_1, {'from': accounts[0]})
    MyUniswapV3ExchangeAdd.modifyPositionForUniV3NFLP(token_id_1, modifyParams, {'from': accounts[0], 'value': 5 * 10 ** 15})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))

    modifyParams = [3000, -120000, -60000, accounts[0], 2 ** 256 - 1]
    print("-----STEP10-----")
    MyNonfungiblePositionManager.approve(MyUniswapV3ExchangeAdd, token_id_2, {'from': accounts[0]})
    MyUniswapV3ExchangeAdd.modifyPositionForUniV3NFLP(token_id_2, modifyParams, {'from': accounts[0], 'value': 5 * 10 ** 15})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))

    modifyParams = [3000, -120000, -60000, accounts[0], 2 ** 256 - 1]
    print("-----STEP11-----")
    MyNonfungiblePositionManager.approve(MyUniswapV3ExchangeAdd, token_id_3, {'from': accounts[0]})
    tx2 = MyUniswapV3ExchangeAdd.modifyPositionForUniV3NFLP(token_id_3, modifyParams, {'from': accounts[0], 'value': 5 * 10 ** 15})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))

    modifyParams = [500, -120000, -60000, accounts[0], 2 ** 256 - 1]
    print("-----STEP12-----")
    MyNonfungiblePositionManager.approve(MyUniswapV3ExchangeAdd, token_id_4, {'from': accounts[0]})
    tx1 = MyUniswapV3ExchangeAdd.modifyPositionForUniV3NFLP(token_id_4, modifyParams, {'from': accounts[0], 'value': 5 * 10 ** 15})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))

    liq = tx1.events['IncreaseLiquidity']['liquidity']
    removeParams = [liq // 2, accounts[0], 2 ** 256 - 1]
    token_id = MyNonfungiblePositionManager.tokenOfOwnerByIndex(accounts[0], MyNonfungiblePositionManager.balanceOf(accounts[0]) - 1)
    print("-----STEP13-----")
    MyNonfungiblePositionManager.approve(MyUniswapV3ExchangeRemove, token_id, {'from': accounts[0]})
    tx = MyUniswapV3ExchangeRemove.removeLiquidityEthFromUniV3NFLP(token_id, removeParams, {'from': accounts[0], 'value': 5 * 10 ** 15})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))

    removeParams = [liq - liq // 2, accounts[0], 2 ** 256 - 1]
    token_id = MyNonfungiblePositionManager.tokenOfOwnerByIndex(accounts[0], MyNonfungiblePositionManager.balanceOf(accounts[0]) - 1)
    print("-----STEP14-----")
    MyNonfungiblePositionManager.approve(MyUniswapV3ExchangeRemove, token_id, {'from': accounts[0]})
    MyUniswapV3ExchangeRemove.removeLiquidityFromUniV3NFLP(token_id, removeParams, {'from': accounts[0], 'value': 5 * 10 ** 15})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))

    liq = tx2.events['IncreaseLiquidity']['liquidity']
    removeParams = [liq // 2, accounts[0], 2 ** 256 - 1]
    token_id = MyNonfungiblePositionManager.tokenOfOwnerByIndex(accounts[0], MyNonfungiblePositionManager.balanceOf(accounts[0]) - 1)
    print("-----STEP15-----")
    MyNonfungiblePositionManager.approve(MyUniswapV3ExchangeRemove, token_id, {'from': accounts[0]})
    MyUniswapV3ExchangeRemove.divestUniV3NFLPToToken(token_id, "0x0000000000000000000000000000000000000000", removeParams, 0, {'from': accounts[0], 'value': 5 * 10 ** 15})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("USDC Balance")
    print(USDC.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))

    removeParams = [liq - liq // 2, accounts[0], 2 ** 256 - 1]
    token_id = MyNonfungiblePositionManager.tokenOfOwnerByIndex(accounts[0], MyNonfungiblePositionManager.balanceOf(accounts[0]) - 1)
    print("-----STEP16-----")
    MyNonfungiblePositionManager.approve(MyUniswapV3ExchangeRemove, token_id, {'from': accounts[0]})
    MyUniswapV3ExchangeRemove.divestUniV3NFLPToToken(token_id, USDC, removeParams, 0, {'from': accounts[0], 'value': 5 * 10 ** 15})
    print("NFT Balance")
    print(MyNonfungiblePositionManager.balanceOf(accounts[0]))
    print("Eth Balance")
    print(accounts[0].balance())
    print("WETH Balance")
    print(WETH.balanceOf(accounts[0]))
    print("DAI Balance")
    print(DAI.balanceOf(accounts[0]))
    print("USDC Balance")
    print(USDC.balanceOf(accounts[0]))
    print("Contract Balances")
    print(MyNonfungiblePositionManager.balance())
    print(WETH.balanceOf(MyUniswapV3ExchangeAdd))
    print(DAI.balanceOf(MyUniswapV3ExchangeAdd))

def getSqrtRatioAtTick(tick: int):
    assert tick >= -887272 and tick <= 887272
    absTick = 0
    if tick > 0:
        absTick = tick
    else:
        absTick = -tick

    ratio = 0x100000000000000000000000000000000
    if absTick & 0x1 != 0:
        ratio = 0xfffcb933bd6fad37aa2d162d1a594001
    if absTick & 0x2 != 0:
        ratio = (ratio * 0xfff97272373d413259a46990580e213a) >> 128
    if absTick & 0x4 != 0:
        ratio = (ratio * 0xfff2e50f5f656932ef12357cf3c7fdcc) >> 128
    if absTick & 0x8 != 0:
        ratio = (ratio * 0xffe5caca7e10e4e61c3624eaa0941cd0) >> 128
    if absTick & 0x10 != 0:
        ratio = (ratio * 0xffcb9843d60f6159c9db58835c926644) >> 128
    if absTick & 0x20 != 0:
        ratio = (ratio * 0xff973b41fa98c081472e6896dfb254c0) >> 128
    if absTick & 0x40 != 0:
        ratio = (ratio * 0xff2ea16466c96a3843ec78b326b52861) >> 128
    if absTick & 0x80 != 0:
        ratio = (ratio * 0xfe5dee046a99a2a811c461f1969c3053) >> 128
    if absTick & 0x100 != 0:
        ratio = (ratio * 0xfcbe86c7900a88aedcffc83b479aa3a4) >> 128
    if absTick & 0x200 != 0:
        ratio = (ratio * 0xf987a7253ac413176f2b074cf7815e54) >> 128
    if absTick & 0x400 != 0:
        ratio = (ratio * 0xf3392b0822b70005940c7a398e4b70f3) >> 128
    if absTick & 0x800 != 0:
        ratio = (ratio * 0xe7159475a2c29b7443b29c7fa6e889d9) >> 128
    if absTick & 0x1000 != 0:
        ratio = (ratio * 0xd097f3bdfd2022b8845ad8f792aa5825) >> 128
    if absTick & 0x2000 != 0:
        ratio = (ratio * 0xa9f746462d870fdf8a65dc1f90e061e5) >> 128
    if absTick & 0x4000 != 0:
        ratio = (ratio * 0x70d869a156d2a1b890bb3df62baf32f7) >> 128
    if absTick & 0x8000 != 0:
        ratio = (ratio * 0x31be135f97d08fd981231505542fcfa6) >> 128
    if absTick & 0x10000 != 0:
        ratio = (ratio * 0x9aa508b5b7a84e1c677de54f3e99bc9) >> 128
    if absTick & 0x20000 != 0:
        ratio = (ratio * 0x5d6af8dedb81196699c329225ee604) >> 128
    if absTick & 0x40000 != 0:
        ratio = (ratio * 0x2216e584f5fa1ea926041bedfe98) >> 128
    if absTick & 0x80000 != 0:
        ratio = (ratio * 0x48a170391f7dc42444e8fa2) >> 128
    if tick > 0:
        ratio = (1 << 256) // ratio
    
    if ratio % (1 << 32) > 0:
        return (ratio >> 32) + 1
    else:
        return ratio >> 32
