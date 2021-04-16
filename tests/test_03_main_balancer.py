#!/usr/bin/python3

import pytest
from brownie.test import strategy
from hypothesis import HealthCheck

class StateMachine:

    coin = strategy('uint16', max_value=6)
    pool = strategy('uint16', max_value=4)
    valueEth = strategy('uint256', min_value=9 * 10 ** 17, max_value=11 * 10 ** 17)
    valueUSD6 = strategy('uint256', min_value=900 * 10 ** 6, max_value=1100 * 10 ** 6)
    valueUSD18 = strategy('uint256', min_value=900 * 10 ** 18, max_value=1100 * 10 ** 18)
    valueBTC = strategy('uint256', min_value=9 * 10 ** 6, max_value=11 * 10 ** 6)

    def __init__(self, MyBalancerExchangeAdd, UniswapV2Router02, DAI, USDC, USDT, WETH, WBTC, accounts, Contract):
        self.coins = [
            "0x0000000000000000000000000000000000000000",
            "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
            WETH,
            USDC,
            DAI,
            USDT,
            WBTC
        ]
        self.MyBalancerExchangeAdd = MyBalancerExchangeAdd
        self.accounts = accounts
        self.Contract = Contract
        self.WETH = WETH
        self.USDT = USDT
        self.USDC = USDC
        UniswapV2Router02.swapETHForExactTokens(5000 * 10 ** 6, [WETH, USDC], accounts[0], 2 ** 256 - 1, {"from":accounts[0], "value": 10 * 10 ** 18})
        UniswapV2Router02.swapETHForExactTokens(5000 * 10 ** 6, [WETH, USDT], accounts[0], 2 ** 256 - 1, {"from":accounts[0], "value": 10 * 10 ** 18})
        UniswapV2Router02.swapETHForExactTokens(5000 * 10 ** 18, [WETH, DAI], accounts[0], 2 ** 256 - 1, {"from":accounts[0], "value": 10 * 10 ** 18})
        WETH.deposit({"from":accounts[0], "value": 5 * 10 ** 18})
        UniswapV2Router02.swapETHForExactTokens(5 * 10 ** 7, [WETH, WBTC], accounts[0], 2 ** 256 - 1, {"from":accounts[0], "value": 50 * 10 ** 18})

    def rule_any_pair_test(self, coin, pool, valueEth, valueUSD6, valueUSD18, valueBTC):
        values = [
                valueEth,
                valueEth,
                valueEth,
                valueUSD6,
                valueUSD18,
                valueUSD6,
                valueBTC
            ]

        pools = [
            "0x1efF8aF5D577060BA4ac8A29A13525bb0Ee2A3D5", # WETH/WBTC 50/50
            "0x59A19D8c652FA0284f44113D0ff9aBa70bd46fB4", # BAL/ETH 80/20
            "0x8b6e6E7B5b3801FEd2CaFD4b22b8A16c2F2Db21a", # DAI/ETH 20/80
            "0xE3f9cF7D44488715361581DD8B3a15379953eB4C", # SNX/ETH/xSNXa 25/25/50
            "0x5B2dC8c02728e8FB6aeA03a622c3849875A48801"  # wPE/GIFT/IMPACT/YFU/PIXEL/NFTS/LIFT/STR 86/2/2/2/2/2/2/2
            ]

        accounts = self.accounts
        coins = self.coins
        Contract = self.Contract
        MyBalancerExchangeAdd = self.MyBalancerExchangeAdd
        print("Test coin " + str(coin))
        print("Test pool " + str(pool))
        pair = Contract.from_abi("BPT", pools[pool], [{"inputs":[],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"src","type":"address"},{"indexed":True,"internalType":"address","name":"dst","type":"address"},{"indexed":False,"internalType":"uint256","name":"amt","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":True,"inputs":[{"indexed":True,"internalType":"bytes4","name":"sig","type":"bytes4"},{"indexed":True,"internalType":"address","name":"caller","type":"address"},{"indexed":False,"internalType":"bytes","name":"data","type":"bytes"}],"name":"LOG_CALL","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"caller","type":"address"},{"indexed":True,"internalType":"address","name":"tokenOut","type":"address"},{"indexed":False,"internalType":"uint256","name":"tokenAmountOut","type":"uint256"}],"name":"LOG_EXIT","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"caller","type":"address"},{"indexed":True,"internalType":"address","name":"tokenIn","type":"address"},{"indexed":False,"internalType":"uint256","name":"tokenAmountIn","type":"uint256"}],"name":"LOG_JOIN","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"caller","type":"address"},{"indexed":True,"internalType":"address","name":"tokenIn","type":"address"},{"indexed":True,"internalType":"address","name":"tokenOut","type":"address"},{"indexed":False,"internalType":"uint256","name":"tokenAmountIn","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"tokenAmountOut","type":"uint256"}],"name":"LOG_SWAP","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"src","type":"address"},{"indexed":True,"internalType":"address","name":"dst","type":"address"},{"indexed":False,"internalType":"uint256","name":"amt","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":True,"inputs":[],"name":"BONE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"BPOW_PRECISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"EXIT_FEE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"INIT_POOL_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MAX_BOUND_TOKENS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MAX_BPOW_BASE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MAX_FEE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MAX_IN_RATIO","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MAX_OUT_RATIO","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MAX_TOTAL_WEIGHT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MAX_WEIGHT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MIN_BALANCE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MIN_BOUND_TOKENS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MIN_BPOW_BASE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MIN_FEE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MIN_WEIGHT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"amt","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"whom","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"denorm","type":"uint256"}],"name":"bind","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"tokenBalanceIn","type":"uint256"},{"internalType":"uint256","name":"tokenWeightIn","type":"uint256"},{"internalType":"uint256","name":"tokenBalanceOut","type":"uint256"},{"internalType":"uint256","name":"tokenWeightOut","type":"uint256"},{"internalType":"uint256","name":"tokenAmountOut","type":"uint256"},{"internalType":"uint256","name":"swapFee","type":"uint256"}],"name":"calcInGivenOut","outputs":[{"internalType":"uint256","name":"tokenAmountIn","type":"uint256"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"tokenBalanceIn","type":"uint256"},{"internalType":"uint256","name":"tokenWeightIn","type":"uint256"},{"internalType":"uint256","name":"tokenBalanceOut","type":"uint256"},{"internalType":"uint256","name":"tokenWeightOut","type":"uint256"},{"internalType":"uint256","name":"tokenAmountIn","type":"uint256"},{"internalType":"uint256","name":"swapFee","type":"uint256"}],"name":"calcOutGivenIn","outputs":[{"internalType":"uint256","name":"tokenAmountOut","type":"uint256"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"tokenBalanceOut","type":"uint256"},{"internalType":"uint256","name":"tokenWeightOut","type":"uint256"},{"internalType":"uint256","name":"poolSupply","type":"uint256"},{"internalType":"uint256","name":"totalWeight","type":"uint256"},{"internalType":"uint256","name":"tokenAmountOut","type":"uint256"},{"internalType":"uint256","name":"swapFee","type":"uint256"}],"name":"calcPoolInGivenSingleOut","outputs":[{"internalType":"uint256","name":"poolAmountIn","type":"uint256"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"tokenBalanceIn","type":"uint256"},{"internalType":"uint256","name":"tokenWeightIn","type":"uint256"},{"internalType":"uint256","name":"poolSupply","type":"uint256"},{"internalType":"uint256","name":"totalWeight","type":"uint256"},{"internalType":"uint256","name":"tokenAmountIn","type":"uint256"},{"internalType":"uint256","name":"swapFee","type":"uint256"}],"name":"calcPoolOutGivenSingleIn","outputs":[{"internalType":"uint256","name":"poolAmountOut","type":"uint256"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"tokenBalanceIn","type":"uint256"},{"internalType":"uint256","name":"tokenWeightIn","type":"uint256"},{"internalType":"uint256","name":"poolSupply","type":"uint256"},{"internalType":"uint256","name":"totalWeight","type":"uint256"},{"internalType":"uint256","name":"poolAmountOut","type":"uint256"},{"internalType":"uint256","name":"swapFee","type":"uint256"}],"name":"calcSingleInGivenPoolOut","outputs":[{"internalType":"uint256","name":"tokenAmountIn","type":"uint256"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"tokenBalanceOut","type":"uint256"},{"internalType":"uint256","name":"tokenWeightOut","type":"uint256"},{"internalType":"uint256","name":"poolSupply","type":"uint256"},{"internalType":"uint256","name":"totalWeight","type":"uint256"},{"internalType":"uint256","name":"poolAmountIn","type":"uint256"},{"internalType":"uint256","name":"swapFee","type":"uint256"}],"name":"calcSingleOutGivenPoolIn","outputs":[{"internalType":"uint256","name":"tokenAmountOut","type":"uint256"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"tokenBalanceIn","type":"uint256"},{"internalType":"uint256","name":"tokenWeightIn","type":"uint256"},{"internalType":"uint256","name":"tokenBalanceOut","type":"uint256"},{"internalType":"uint256","name":"tokenWeightOut","type":"uint256"},{"internalType":"uint256","name":"swapFee","type":"uint256"}],"name":"calcSpotPrice","outputs":[{"internalType":"uint256","name":"spotPrice","type":"uint256"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"amt","type":"uint256"}],"name":"decreaseApproval","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"uint256","name":"poolAmountIn","type":"uint256"},{"internalType":"uint256[]","name":"minAmountsOut","type":"uint256[]"}],"name":"exitPool","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"tokenAmountOut","type":"uint256"},{"internalType":"uint256","name":"maxPoolAmountIn","type":"uint256"}],"name":"exitswapExternAmountOut","outputs":[{"internalType":"uint256","name":"poolAmountIn","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"poolAmountIn","type":"uint256"},{"internalType":"uint256","name":"minAmountOut","type":"uint256"}],"name":"exitswapPoolAmountIn","outputs":[{"internalType":"uint256","name":"tokenAmountOut","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[],"name":"finalize","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getColor","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getController","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getCurrentTokens","outputs":[{"internalType":"address[]","name":"tokens","type":"address[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"getDenormalizedWeight","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getFinalTokens","outputs":[{"internalType":"address[]","name":"tokens","type":"address[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"getNormalizedWeight","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getNumTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"}],"name":"getSpotPrice","outputs":[{"internalType":"uint256","name":"spotPrice","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"}],"name":"getSpotPriceSansFee","outputs":[{"internalType":"uint256","name":"spotPrice","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getSwapFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getTotalDenormalizedWeight","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"gulp","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"amt","type":"uint256"}],"name":"increaseApproval","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"t","type":"address"}],"name":"isBound","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"isFinalized","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"isPublicSwap","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"uint256","name":"poolAmountOut","type":"uint256"},{"internalType":"uint256[]","name":"maxAmountsIn","type":"uint256[]"}],"name":"joinPool","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"tokenAmountIn","type":"uint256"},{"internalType":"uint256","name":"minPoolAmountOut","type":"uint256"}],"name":"joinswapExternAmountIn","outputs":[{"internalType":"uint256","name":"poolAmountOut","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"poolAmountOut","type":"uint256"},{"internalType":"uint256","name":"maxAmountIn","type":"uint256"}],"name":"joinswapPoolAmountOut","outputs":[{"internalType":"uint256","name":"tokenAmountIn","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"denorm","type":"uint256"}],"name":"rebind","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"manager","type":"address"}],"name":"setController","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"bool","name":"public_","type":"bool"}],"name":"setPublicSwap","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"uint256","name":"swapFee","type":"uint256"}],"name":"setSwapFee","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"tokenAmountIn","type":"uint256"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"minAmountOut","type":"uint256"},{"internalType":"uint256","name":"maxPrice","type":"uint256"}],"name":"swapExactAmountIn","outputs":[{"internalType":"uint256","name":"tokenAmountOut","type":"uint256"},{"internalType":"uint256","name":"spotPriceAfter","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"maxAmountIn","type":"uint256"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"tokenAmountOut","type":"uint256"},{"internalType":"uint256","name":"maxPrice","type":"uint256"}],"name":"swapExactAmountOut","outputs":[{"internalType":"uint256","name":"tokenAmountIn","type":"uint256"},{"internalType":"uint256","name":"spotPriceAfter","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"amt","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"amt","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"unbind","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"}])
        
        print(pair.balanceOf(accounts[0]))
        if coin < 2:
            print(accounts[0].balance())
            MyBalancerExchangeAdd.investTokenForBalancerPoolToken(coins[coin], pair, values[coin], 1, {"from":accounts[0], "value": values[coin] + 5 * 10 ** 15})
            print(accounts[0].balance())
        else:
            print(coins[coin].balanceOf(accounts[0]))
            if coins[coin].allowance(accounts[0], MyBalancerExchangeAdd) == 0:
                coins[coin].approve(MyBalancerExchangeAdd, 2 ** 256 - 1, {"from": accounts[0]})
            MyBalancerExchangeAdd.investTokenForBalancerPoolToken(coins[coin], pair, values[coin], 1, {"from":accounts[0], "value": 5 * 10 ** 15})
            print(coins[coin].balanceOf(accounts[0]))
        print(pair.balanceOf(accounts[0]))

def test_main(MyBalancerExchangeAdd, MySushiswapExchangeRemove, UniswapV2Router02, SushiswapFactory, DAI, USDC, USDT, WETH, WBTC, accounts, Contract, state_machine):
    settings = {"suppress_health_check": HealthCheck.all(), "max_examples": 20}
    state_machine(StateMachine, MyBalancerExchangeAdd, UniswapV2Router02, DAI, USDC, USDT, WETH, WBTC, accounts, Contract, settings=settings)
