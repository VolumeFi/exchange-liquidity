# @version 0.2.12

interface ERC20:
    def allowance(owner: address, spender: address) -> uint256: view

interface BFactory:
    def isBPool(b: address) -> bool: view

interface BPool:
    def exitswapPoolAmountIn(tokenOut: address, poolAmountIn: uint256, minAmountOut: uint256) -> uint256: nonpayable
    def isBound(t: address) -> bool: view
    def getNumTokens() -> uint256: view

interface UniswapV2Factory:
    def getPair(tokenA: address, tokenB: address) -> address: view

interface UniswapV2Pair:
    def token0() -> address: view
    def token1() -> address: view
    def getReserves() -> (uint256, uint256, uint256): view

interface WrappedEth:
    def withdraw(amount: uint256): nonpayable

event LPTokenBurn:
    lptoken: address
    recipient: address
    liquidity: uint256

event Paused:
    paused: bool

event FeeChanged:
    newFee: uint256

UNISWAPV2ROUTER02: constant(address) = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D
UNISWAPV2FACTORY: constant(address) = 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f
BALANCERFACTORY: constant(address) = 0x9424B1412450D0f8Fc2255FAf6046b98213B76Bd
VETH: constant(address) = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
WETH: constant(address) = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
DEADLINE: constant(uint256) = MAX_UINT256 # change

TRANSFERFROM_MID: constant(Bytes[4]) = method_id("transferFrom(address,address,uint256)")
TRANSFER_MID: constant(Bytes[4]) = method_id("transfer(address,uint256)")
APPROVE_MID: constant(Bytes[4]) = method_id("approve(address,uint256)")
SWAPETFT_MID: constant(Bytes[4]) = method_id("swapExactTokensForTokens(uint256,uint256,address[],address,uint256)")
GETCURRENTTOKENS_MID: constant(Bytes[4]) = method_id("getCurrentTokens()")

paused: public(bool)
admin: public(address)
feeAmount: public(uint256)
feeAddress: public(address)

@external
def __init__():
    self.paused = False
    self.admin = msg.sender
    self.feeAddress = 0xf29399fB3311082d9F8e62b988cBA44a5a98ebeD
    self.feeAmount = 5 * 10 ** 15

@internal
def safeApprove(_token: address, _spender: address, _value: uint256):
    _response: Bytes[32] = raw_call(
        _token,
        concat(
            APPROVE_MID,
            convert(_spender, bytes32),
            convert(_value, bytes32)
        ),
        max_outsize=32
    )  # dev: failed approve
    if len(_response) > 0:
        assert convert(_response, bool), "Approve failed"  # dev: failed approve

@internal
def safeTransfer(_token: address, _to: address, _value: uint256):
    _response: Bytes[32] = raw_call(
        _token,
        concat(
            TRANSFER_MID,
            convert(_to, bytes32),
            convert(_value, bytes32)
        ),
        max_outsize=32
    )  # dev: failed transfer
    if len(_response) > 0:
        assert convert(_response, bool), "Transfer failed"  # dev: failed transfer

@internal
def safeTransferFrom(_token: address, _from: address, _to: address, _value: uint256):
    _response: Bytes[32] = raw_call(
        _token,
        concat(
            TRANSFERFROM_MID,
            convert(_from, bytes32),
            convert(_to, bytes32),
            convert(_value, bytes32)
        ),
        max_outsize=32
    )  # dev: failed transferFrom
    if len(_response) > 0:
        assert convert(_response, bool), "TransferFrom failed"  # dev: failed transferFrom

@internal
def _exitFromBalancer(_fromBalancerPoolAddress: address, _toTokenContractAddress: address, tokens2Trade: uint256) -> uint256:
    assert BPool(_fromBalancerPoolAddress).isBound(_toTokenContractAddress), "Token not bound"
    tokensOut: uint256 = BPool(_fromBalancerPoolAddress).exitswapPoolAmountIn(_toTokenContractAddress, tokens2Trade, 1)
    assert tokensOut > 0, "Error in exiting balancer pool"
    return tokensOut


@internal
@pure
def _getPairTokens(pair: address) -> (address, address):
    token0: address = UniswapV2Pair(pair).token0()
    token1: address = UniswapV2Pair(pair).token1()
    return (token0, token1)

@internal
@view
def _getLiquidityInPool(midToken: address, pair: address) -> uint256:
    res0: uint256 = 0
    res1: uint256 = 0
    token0: address = ZERO_ADDRESS
    token1: address = ZERO_ADDRESS
    blockTimestampLast: uint256 = 0
    (res0, res1, blockTimestampLast) = UniswapV2Pair(pair).getReserves()
    (token0, token1) = self._getPairTokens(pair)
    if token0 == midToken:
        return res0
    else:
        return res1

@internal
@view
def _getMidTokenNumber(midToken: address, tokens: address[8]) -> uint256:
    maxeth: uint256 = 0
    maxi: uint256 = 0
    for i in range(8):
        if tokens[i] == ZERO_ADDRESS:
            break
        if midToken == tokens[i]:
            return i
        pair: address = UniswapV2Factory(UNISWAPV2FACTORY).getPair(midToken, tokens[i])
        eth: uint256 = 0
        if pair != ZERO_ADDRESS:
            eth = self._getLiquidityInPool(midToken, pair)
        if eth > maxeth:
            maxeth = eth
            maxi = i
    return maxi

@internal
def _token2Token(fromToken: address, toToken: address, tokens2Trade: uint256, deadline: uint256) -> uint256:
    if fromToken == toToken:
        return tokens2Trade
    _response32: Bytes[32] = empty(Bytes[32])
    if ERC20(fromToken).allowance(self, UNISWAPV2ROUTER02) > 0:
        self.safeApprove(fromToken, UNISWAPV2ROUTER02, 0)
    self.safeApprove(fromToken, UNISWAPV2ROUTER02, tokens2Trade)
    _response128: Bytes[128] = raw_call(
        UNISWAPV2ROUTER02,
        concat(
            SWAPETFT_MID,
            convert(tokens2Trade, bytes32),
            convert(0, bytes32),
            convert(160, bytes32),
            convert(self, bytes32),
            convert(deadline, bytes32),
            convert(2, bytes32),
            convert(fromToken, bytes32),
            convert(toToken, bytes32)
        ),
        max_outsize=128
    )
    tokenBought: uint256 = convert(slice(_response128, 96, 32), uint256)
    assert tokenBought > 0, "Error Swapping Token 2"
    return tokenBought

@internal
def _exitFromBalancerViaUniswap(_fromBalancerPoolAddress: address, _toTokenContractAddress: address, _tokens2Trade: uint256) -> uint256:
    numTokens: uint256 = BPool(_fromBalancerPoolAddress).getNumTokens()    
    _response320: Bytes[320] = raw_call(
        _fromBalancerPoolAddress,
        GETCURRENTTOKENS_MID,
        is_static_call=True,
        max_outsize=320
    )
    tokens: address[8] = [ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS]
    for i in range(8):
        tokens[i] = convert(convert(slice(_response320, 32 * (i + 2), 32), uint256), address)
        if i == (numTokens - 1):
            break
    midTokenNumber: uint256 = self._getMidTokenNumber(WETH, tokens)
    tokens2Trade: uint256 = self._exitFromBalancer(_fromBalancerPoolAddress, tokens[midTokenNumber], _tokens2Trade)
    
    tokens2Trade = self._token2Token(tokens[midTokenNumber], WETH, tokens2Trade, DEADLINE)
    tokens2Trade = self._token2Token(WETH, _toTokenContractAddress, tokens2Trade, DEADLINE)
    return tokens2Trade

@external
@payable
@nonreentrant('lock')
def divestBalancerPoolTokenToToken(_token: address, _pair: address, bptAmount: uint256, minTokenAmount: uint256, deadline: uint256=DEADLINE) -> uint256:
    assert bptAmount > 0, "Invalid input amount"
    assert block.timestamp <= deadline, "Expired"
    assert not self.paused, "Paused"
    assert BFactory(BALANCERFACTORY).isBPool(_pair), "!Balancer Pool"
    fee: uint256 = self.feeAmount
    if msg.value > fee:
        send(self.feeAddress, fee)
        send(msg.sender, msg.value - fee)
    else:
        assert msg.value == fee, "Insufficient fee"
        send(self.feeAddress, fee)
    
    self.safeTransferFrom(_pair, msg.sender, self, bptAmount)

    token: address = _token
    if _token == VETH or _token == ZERO_ADDRESS:
        token = WETH
    isBound: bool = BPool(_pair).isBound(token)
    tokenAmount: uint256 = 0
    if (isBound):
        tokenAmount = self._exitFromBalancer(_pair, token, bptAmount)
    else:
        tokenAmount = self._exitFromBalancerViaUniswap(_pair, token, bptAmount)

    if _token != token:
        WrappedEth(WETH).withdraw(tokenAmount)
        send(msg.sender, tokenAmount)
    else:
        self.safeTransfer(token, msg.sender, tokenAmount)

    assert tokenAmount >= minTokenAmount, "High Slippage"

    log LPTokenBurn(_pair, msg.sender, bptAmount)

    return tokenAmount

# Admin functions
@external
def pause(_paused: bool):
    assert msg.sender == self.admin, "Not admin"
    self.paused = _paused
    log Paused(_paused)

@external
def newAdmin(_admin: address):
    assert msg.sender == self.admin, "Not admin"
    self.admin = _admin

@external
def newFeeAmount(_feeAmount: uint256):
    assert msg.sender == self.admin, "Not admin"
    self.feeAmount = _feeAmount
    log FeeChanged(_feeAmount)

@external
def newFeeAddress(_feeAddress: address):
    assert msg.sender == self.admin, "Not admin"
    self.feeAddress = _feeAddress

@external
@nonreentrant('lock')
def batchWithdraw(token: address[8], amount: uint256[8], to: address[8]):
    assert msg.sender == self.admin, "Not admin"
    for i in range(8):
        if token[i] == VETH:
            send(to[i], amount[i])
        elif token[i] != ZERO_ADDRESS:
            _response32: Bytes[32] = raw_call(
                token[i],
                concat(
                    TRANSFER_MID,
                    convert(to[i], bytes32),
                    convert(amount[i], bytes32),
                ),
                max_outsize=32
            )  # dev: failed transfer
            if len(_response32) > 0:
                assert convert(_response32, bool), "Transfer failed"  # dev: failed transfer

@external
@nonreentrant('lock')
def withdraw(token: address, amount: uint256, to: address):
    assert msg.sender == self.admin, "Not admin"
    if token == VETH:
        send(to, amount)
    elif token != ZERO_ADDRESS:
        _response32: Bytes[32] = raw_call(
            token,
            concat(
                TRANSFER_MID,
                convert(to, bytes32),
                convert(amount, bytes32),
            ),
            max_outsize=32
        )  # dev: failed transfer
        if len(_response32) > 0:
            assert convert(_response32, bool), "Transfer failed"  # dev: failed transfer

@external
@payable
def __default__():
    assert msg.sender == WETH, "can't receive Eth"