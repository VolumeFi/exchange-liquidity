#!/usr/bin/python3

import pytest
from brownie.test import strategy
from hypothesis import HealthCheck

class StateMachine:

    coin = strategy('uint16', max_value=6)
    valueEth = strategy('uint256', min_value=9 * 10 ** 17, max_value=11 * 10 ** 17)
    valueUSD6 = strategy('uint256', min_value=900 * 10 ** 6, max_value=1100 * 10 ** 6)
    valueUSD18 = strategy('uint256', min_value=900 * 10 ** 18, max_value=1100 * 10 ** 18)
    valueBTC = strategy('uint256', min_value=9 * 10 ** 6, max_value=11 * 10 ** 6)
    pool = strategy('uint16', max_value=31)

    def __init__(self, MyCurveExchangeAdd, MyCurveExchangeRemove, UniswapV2Router02, DAI, USDC, USDT, WETH, WBTC, accounts, Contract):
        self.coins = [
            "0x0000000000000000000000000000000000000000",
            "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
            USDC,
            DAI,
            USDT,
            WETH,
            WBTC
        ]
        self.pools = [
            "0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56",
            "0x52EA46506B9CC5Ef470C5bf89f17Dc28bB35D85C",
            "0x06364f10B501e868329afBc005b3492902d6C763",
            "0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51",
            "0x79a8C46DeA5aDa233ABaFFD40F3A0A2B1e5A4F27",
            "0xA5407eAE9Ba41422680e2e00537571bcC53efBfD",
            "0x93054188d876f558f4a66B2EF1d97d16eDf0895B",
            "0x7fC77b5c7614E1533320Ea6DDc2Eb61fa00A9714",
            "0x4CA9b3063Ec5866A4B82E437059D2C43d1be596F",
            "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7",
            "0x4f062658EaAF2C1ccf8C8e36D6824CDf41167956",
            "0x3eF6A01A0f81D6046290f3e2A8c5b843e738E604",
            "0x3E01dD8a5E1fb3481F0F589056b428Fc308AF0Fb",
            "0x0f9cb53Ebe405d49A0bbdBD291A65Ff571bC83e1",
            "0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171",
            "0x8474DdbE98F5aA3179B3B3F5942D724aFcdec9f6",
            "0xC18cC39da8b11dA8c3541C598eE022258F9744da",
            "0xC25099792E9349C7DD09759744ea681C7de2cb66",
            "0x8038C01A0390a8c547446a0b2c18fc9aEFEcc10c",
            "0x7F55DDe206dbAD629C080068923b36fe9D6bDBeF",
            "0x071c661B4DeefB59E2a3DdB20Db036821eeE8F4b",
            "0xd81dA8D904b52208541Bade1bD6595D8a251F8dd",
            "0x890f4e345B1dAED0367A877a1612f86A1f86985f",
            "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA",
            "0xc5424B857f758E906013F3555Dad202e4bdB4567",
            "0xDeBF20617708857ebe4F679508E7b7863a8A8EeE",
            "0xDC24316b9AE028F1497c275EB9192a3Ea0f67022",
            "0xEB16Ae0052ed37f479f7fe63849198Df1765a733",
            "0xA96A65c051bF88B4095Ee1f2451C2A9d43F53Ae2",
            "0x42d7025938bEc20B69cBae5A77421082407f053A",
            "0x2dded6Da1BF5DBdF597C45fcFaa3194e53EcfeAF",
            "0xF178C0b5Bb7e7aBF4e12A4838C7b7c5bA2C623c0"
        ]
        self.tokens = [
            "0x845838DF265Dcd2c412A1Dc9e959c7d08537f8a2",
            "0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23",
            "0xD905e2eaeBe188fc92179b6350807D8bd91Db0D8",
            "0xdF5e0e81Dff6FAF3A7e52BA697820c5e32D806A8",
            "0x3B3Ac5386837Dc563660FB6a0937DFAa5924333B",
            "0xC25a3A3b969415c80451098fa907EC722572917F",
            "0x49849C98ae39Fff122806C06791Fa73784FB3675",
            "0x075b1bb99792c9E1041bA13afEf80C91a1e70fB3",
            "0xb19059ebb43466C323583928285a49f558E572Fd",
            "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490",
            "0xD2967f45c4f384DEEa880F807Be904762a3DeA07",
            "0x5B5CFE992AdAC0C9D48E05854B2d91C73a003858",
            "0x97E2768e8E73511cA874545DC5Ff8067eB19B787",
            "0x4f3E8F405CF5aFC05D68142F3783bDfE13811522",
            "0x6D65b498cb23deAba52db31c93Da9BFFb340FB8F",
            "0x1AEf73d49Dedc4b1778d0706583995958Dc862e6",
            "0xC2Ee6b0334C261ED60C72f6054450b61B8f18E35",
            "0x64eda51d3Ad40D56b9dFc5554E06F94e1Dd786Fd",
            "0x3a664Ab939FD8482048609f652f9a0B0677337B9",
            "0xDE5331AC4B3630f94853Ff322B66407e0D6331E8",
            "0x410e3E86ef427e30B9235497143881f717d93c2A",
            "0x2fE94ea3d5d4a175184081439753DE15AeF9d614",
            "0x94e131324b6054c0D789b190b2dAC504e4361b53",
            "0x194eBd173F6cDacE046C53eACcE9B953F28411d1",
            "0xA3D87FffcE63B53E0d54fAa1cc983B7eB0b74A9c",
            "0xFd2a8fA60Abd58Efe3EeE34dd494cD491dC14900",
            "0x06325440D014e39736583c165C2963BA99fAf14E",
            "0x02d341CcB60fAaf662bC0554d13778015d1b285C",
            "0xaA17A236F2bAdc98DDc0Cf999AbB47D47Fc0A6Cf",
            "0x7Eb40E450b9655f4B3cC4259BCC731c63ff55ae6",
            "0x5282a4eF67D9C33135340fB3289cc1711c13638C",
            "0xcee60cFa923170e4f8204AE08B4fA6A3F5656F3a",        
        ]
        self.MyCurveExchangeAdd = MyCurveExchangeAdd
        self.MyCurveExchangeRemove = MyCurveExchangeRemove
        self.accounts = accounts
        self.Contract = Contract
        UniswapV2Router02.swapETHForExactTokens(40000 * 10 ** 6, [WETH, USDC], accounts[0], 2 ** 256 - 1, {"from":accounts[0], "value": 100 * 10 ** 18})
        UniswapV2Router02.swapETHForExactTokens(40000 * 10 ** 6, [WETH, USDT], accounts[0], 2 ** 256 - 1, {"from":accounts[0], "value": 100 * 10 ** 18})
        UniswapV2Router02.swapETHForExactTokens(40000 * 10 ** 18, [WETH, DAI], accounts[0], 2 ** 256 - 1, {"from":accounts[0], "value": 100 * 10 ** 18})
        WETH.deposit({"from":accounts[0], "value": 40 * 10 ** 18})
        UniswapV2Router02.swapETHForExactTokens(4 * 10 ** 8, [WETH, WBTC], accounts[0], 2 ** 256 - 1, {"from":accounts[0], "value": 200 * 10 ** 18})

    def rule_test(self, coin, valueEth, valueUSD6, valueUSD18, valueBTC, pool):
        values = [
                valueEth,
                valueEth,
                valueUSD6,
                valueUSD18,
                valueUSD6,
                valueEth,
                valueBTC
            ]
        accounts = self.accounts
        lpToken = self.Contract.from_abi("CrvLPToken", self.tokens[pool], [{"name":"Transfer","inputs":[{"type":"address","name":"_from","indexed":True},{"type":"address","name":"_to","indexed":True},{"type":"uint256","name":"_value","indexed":False}],"anonymous":False,"type":"event"},{"name":"Approval","inputs":[{"type":"address","name":"_owner","indexed":True},{"type":"address","name":"_spender","indexed":True},{"type":"uint256","name":"_value","indexed":False}],"anonymous":False,"type":"event"},{"outputs":[],"inputs":[{"type":"string","name":"_name"},{"type":"string","name":"_symbol"}],"stateMutability":"nonpayable","type":"constructor"},{"name":"decimals","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":261},{"name":"transfer","outputs":[{"type":"bool","name":""}],"inputs":[{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"stateMutability":"nonpayable","type":"function","gas":74713},{"name":"transferFrom","outputs":[{"type":"bool","name":""}],"inputs":[{"type":"address","name":"_from"},{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"stateMutability":"nonpayable","type":"function","gas":111355},{"name":"approve","outputs":[{"type":"bool","name":""}],"inputs":[{"type":"address","name":"_spender"},{"type":"uint256","name":"_value"}],"stateMutability":"nonpayable","type":"function","gas":37794},{"name":"increaseAllowance","outputs":[{"type":"bool","name":""}],"inputs":[{"type":"address","name":"_spender"},{"type":"uint256","name":"_added_value"}],"stateMutability":"nonpayable","type":"function","gas":39038},{"name":"decreaseAllowance","outputs":[{"type":"bool","name":""}],"inputs":[{"type":"address","name":"_spender"},{"type":"uint256","name":"_subtracted_value"}],"stateMutability":"nonpayable","type":"function","gas":39062},{"name":"mint","outputs":[{"type":"bool","name":""}],"inputs":[{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"stateMutability":"nonpayable","type":"function","gas":75652},{"name":"burnFrom","outputs":[{"type":"bool","name":""}],"inputs":[{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"stateMutability":"nonpayable","type":"function","gas":75670},{"name":"set_minter","outputs":[],"inputs":[{"type":"address","name":"_minter"}],"stateMutability":"nonpayable","type":"function","gas":36458},{"name":"set_name","outputs":[],"inputs":[{"type":"string","name":"_name"},{"type":"string","name":"_symbol"}],"stateMutability":"nonpayable","type":"function","gas":178219},{"name":"name","outputs":[{"type":"string","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":7763},{"name":"symbol","outputs":[{"type":"string","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":6816},{"name":"balanceOf","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"arg0"}],"stateMutability":"view","type":"function","gas":1636},{"name":"allowance","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"arg0"},{"type":"address","name":"arg1"}],"stateMutability":"view","type":"function","gas":1881},{"name":"totalSupply","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1481},{"name":"minter","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1511}])
        if coin > 1:
            self.coins[coin].approve(self.MyCurveExchangeAdd, values[coin], {"from": accounts[0]})
            self.MyCurveExchangeAdd.investTokenForCrvPair(self.coins[coin], values[coin], self.pools[pool], 1, 2 ** 256 - 1, {"from":accounts[0], "value": 1 * 10 ** 16})
            print("Test pool " + str(pool) + "\ncoin " + str(coin))
            print("Token Amount: " + str(self.coins[coin].balanceOf(accounts[0])))
            print("CrvLPToken : " + str(lpToken.balanceOf(accounts[0])))
            lpToken.approve(self.MyCurveExchangeRemove, lpToken.balanceOf(accounts[0]), {"from":accounts[0]})
            self.MyCurveExchangeRemove.divestTokenForCrvPair(lpToken, lpToken.balanceOf(accounts[0]), self.coins[coin], 1, {"from":accounts[0], "value":1 * 10 ** 16})
            print("Token Amount: " + str(self.coins[coin].balanceOf(accounts[0])))
            print("CrvLPTokenAfterRemove : " + str(lpToken.balanceOf(accounts[0])))
        else:
            self.MyCurveExchangeAdd.investTokenForCrvPair(self.coins[coin], values[coin], self.pools[pool], 1, 2 ** 256 - 1, {"from":accounts[0], "value": values[coin] + 1 * 10 ** 16})
            print("Test pool " + str(pool) + "\ncoin " + str(coin))
            print("Token Amount: " + str(accounts[0].balance()))
            print("CrvLPToken : " + str(lpToken.balanceOf(accounts[0])))
            lpToken.approve(self.MyCurveExchangeRemove, lpToken.balanceOf(accounts[0]), {"from":accounts[0]})
            self.MyCurveExchangeRemove.divestTokenForCrvPair(lpToken, lpToken.balanceOf(accounts[0]), self.coins[coin], 1, {"from":accounts[0], "value":1 * 10 ** 16})
            print("Token Amount: " + str(accounts[0].balance()))
            print("CrvLPTokenAfterRemove : " + str(lpToken.balanceOf(accounts[0])))

def test_main(MyCurveExchangeAdd, MyCurveExchangeRemove, UniswapV2Router02, DAI, USDC, USDT, WETH, WBTC, accounts, Contract, state_machine):
    settings = {"suppress_health_check": HealthCheck.all(), "max_examples": 20}
    state_machine(StateMachine, MyCurveExchangeAdd, MyCurveExchangeRemove, UniswapV2Router02, DAI, USDC, USDT, WETH, WBTC, accounts, Contract, settings=settings)
