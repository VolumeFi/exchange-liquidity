# @version ^0.2.0

interface ERC20:
    def approve(spender: address, amount: uint256): nonpayable
    def transfer(recipient: address, amount: uint256): nonpayable
    def transferFrom(sender: address, recipient: address, amount: uint256): nonpayable
    def allowance(owner: address, spender: address) -> uint256: view
    def balanceOf(account: address) -> uint256: view
    def decimals() -> uint256: view

interface UniswapV2Factory:
    def getPair(token0: address, token1: address) -> address: view

interface UniswapV2Pair:
    def token0() -> address: view
    def token1() -> address: view
    def getReserves() -> (uint256, uint256, uint256): view

interface UniswapV2Router02:
    def addLiquidity(tokenA: address, tokenB: address, amountADesired: uint256, amountBDesired: uint256, amountAMin: uint256, amountBMin: uint256, to: address, deadline: uint256) -> (uint256, uint256, uint256): nonpayable

interface WrappedEth:
    def deposit(): payable

UNISWAPV2FACTORY: constant(address) = 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f
UNISWAPV2ROUTER02: constant(address) = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D

WETH: constant(address) = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
DEADLINE: constant(uint256) = MAX_UINT256

paused: public(bool)
owner: public(address)
feeRate: public(uint256)
feeAddress: public(address)

event TestValue:
    value: uint256
    text: String[256]

event TestAddress:
    addr: address
    text: String[256]

event TestData:
    data: bytes32
    text: String[256]

@external
def __init__():
    self.paused = False
    self.owner = msg.sender

@internal
@pure
def _getPairTokens(pair: address) -> (address, address):
    token0: address = UniswapV2Pair(pair).token0()
    token1: address = UniswapV2Pair(pair).token1()
    return (token0, token1)

@internal
@pure
def uintSqrt(y: uint256) -> uint256:
    z: uint256 = 0
    x: uint256 = 0
    if y > 3:
        z = y
        x = y / 2 + 1
        for i in range(256):
            if x >= z:
                break
            z = x
            x = (y / x + x) / 2
    elif y != 0:
        z = 1
    else:
        z = 0
    return z

@internal
def _wrap(pair: address, amount: uint256) -> (uint256, address):
    token0: address = ZERO_ADDRESS
    token1: address = ZERO_ADDRESS
    (token0, token1) = self._getPairTokens(pair)
    initialBalance0: uint256 = ERC20(token0).balanceOf(self)
    initialBalance1: uint256 = ERC20(token1).balanceOf(self)
    WrappedEth(WETH).deposit(value=amount)
    finalBalance0: uint256 = ERC20(token0).balanceOf(self) - initialBalance0
    finalBalance1: uint256 = ERC20(token1).balanceOf(self) - initialBalance1

    amountBought: uint256 = 0
    intermediateToken: address = ZERO_ADDRESS
    if finalBalance0 > finalBalance1:
        amountBought = finalBalance0
        intermediateToken = token0
    else:
        amountBought = finalBalance1
        intermediateToken = token1
    assert amountBought > 0, "Swapped to Invalid Intermediate"
    return (amountBought, intermediateToken)

@internal
def _token2Token(fromToken: address, toToken: address, tokens2Trade: uint256) -> uint256:
    if fromToken == toToken:
        return tokens2Trade
    if ERC20(fromToken).allowance(self, UNISWAPV2ROUTER02) > 0:
        ERC20(fromToken).approve(UNISWAPV2ROUTER02, 0)
    ERC20(fromToken).approve(UNISWAPV2ROUTER02, tokens2Trade)
    path: address[2] = [ZERO_ADDRESS, ZERO_ADDRESS]
    path[0] = fromToken
    path[1] = toToken
    
    addrBytes: Bytes[288] = concat(convert(tokens2Trade, bytes32), convert(0, bytes32), convert(160, bytes32), convert(self, bytes32), convert(DEADLINE, bytes32), convert(2, bytes32), convert(fromToken, bytes32), convert(toToken, bytes32))
    funcsig: Bytes[4] = method_id("swapExactTokensForTokens(uint256,uint256,address[],address,uint256)")
    full_data: Bytes[292] = concat(funcsig, addrBytes)
    
    _response: Bytes[128] = raw_call(
        UNISWAPV2ROUTER02,
        full_data,
        max_outsize=128
    )
    tokenBought: uint256 = convert(slice(_response, 96, 32), uint256)
    assert tokenBought > 0, "Error Swapping Token 2"
    return tokenBought

@internal
@view
def _calculateSwapInAmount(reserveIn: uint256, userIn: uint256) -> uint256:
    return ((self.uintSqrt(reserveIn * (userIn * 3988000 + reserveIn * 3988009))) - reserveIn * 1997) / 1994

@internal
def _swap(fromToken: address, pair: address, toUnipoolToken0: address, toUnipoolToken1: address, amount: uint256) -> (uint256, uint256):
    res0: uint256 = 0
    res1: uint256 = 0
    blockTimestampLast: uint256 = 0
    (res0, res1, blockTimestampLast) = UniswapV2Pair(pair).getReserves()
    token1Bought: uint256 = 0
    token0Bought: uint256 = 0
    if (fromToken == toUnipoolToken0):
        amountToSwap: uint256 = self._calculateSwapInAmount(res0, amount)
        if amountToSwap == 0:
            amountToSwap = amount / 2
        token1Bought = self._token2Token(fromToken, toUnipoolToken1, amountToSwap)
        token0Bought = amount - amountToSwap
    else:
        amountToSwap: uint256 = self._calculateSwapInAmount(res1, amount)
        if amountToSwap == 0:
            amountToSwap = amount / 2
        token0Bought = self._token2Token(fromToken, toUnipoolToken0, amountToSwap)
        token1Bought = amount - amountToSwap
    return (token0Bought, token1Bought)

@internal
def _uniDeposit(token0: address, token1: address, amount0: uint256, amount1: uint256, sender: address) -> uint256:
    if ERC20(token0).allowance(self, UNISWAPV2ROUTER02) > 0:
        ERC20(token0).approve(UNISWAPV2ROUTER02, 0)
    if ERC20(token1).allowance(self, UNISWAPV2ROUTER02) > 0:
        ERC20(token1).approve(UNISWAPV2ROUTER02, 0)
    ERC20(token0).approve(UNISWAPV2ROUTER02, amount0)
    ERC20(token1).approve(UNISWAPV2ROUTER02, amount1)
    amountA: uint256 = 0
    amountB: uint256 = 0
    LP: uint256 = 0
    (amountA, amountB, LP) = UniswapV2Router02(UNISWAPV2ROUTER02).addLiquidity(token0, token1, amount0, amount1, 1, 1, self, DEADLINE)
    if amount0 - amountA > 0:
        ERC20(token0).transfer(sender, amount0 - amountA)
    if amount1 - amountB > 0:
        ERC20(token1).transfer(sender, amount1 - amountB)
    return LP

@internal
def _performInvest(fromToken:address, pair:address, amount:uint256, sender: address) -> uint256:
    toUniswapToken0: address = ZERO_ADDRESS
    toUniswapToken1: address = ZERO_ADDRESS
    (toUniswapToken0, toUniswapToken1) = self._getPairTokens(pair)
    if fromToken != toUniswapToken0 and fromToken != toUniswapToken1:
        raise "Token Error"
    token0Bought: uint256 = 0
    token1Bought: uint256 = 0
    (token0Bought, token1Bought) = self._swap(fromToken, pair, toUniswapToken0, toUniswapToken1, amount)
    return self._uniDeposit(toUniswapToken0, toUniswapToken1, token0Bought, token1Bought, sender)

@internal
def _transferFee(tokenContractAddress: address, tokens2Trade: uint256) -> uint256:
    feePortion: uint256 = tokens2Trade * self.feeRate / 10000
    if feePortion == 0:
        return 0
    ERC20(tokenContractAddress).transfer(self.feeAddress, feePortion)
    return feePortion

@external
@payable
@nonreentrant('lock')
def invest(fromToken:address, pair:address, amount:uint256, minPoolTokens: uint256) -> uint256:
    assert not self.paused, "Paused"
    toInvest:uint256 = 0
    intermediateToken: address = fromToken
    if fromToken == ZERO_ADDRESS:
        assert msg.value > 0, "ETH not sent"
        toInvest = msg.value
        WrappedEth(WETH).deposit(value=toInvest)
        intermediateToken = WETH
    else:
        assert msg.value == 0, "dev: ETH sent"
        assert amount > 0, "Invalid ERC amount"
        ERC20(fromToken).transferFrom(msg.sender, self, amount)
        toInvest = amount
    LPBought:uint256 = self._performInvest(intermediateToken, pair, toInvest, msg.sender)
    assert LPBought >= minPoolTokens, "High Slippage"
    feePortion: uint256 = self._transferFee(pair, LPBought)
    ERC20(pair).transfer(msg.sender, LPBought - feePortion)
    return LPBought - feePortion

@external
@payable
def __default__(): pass
