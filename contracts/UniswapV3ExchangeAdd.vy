# Copyright (C) 2021 VolumeFi Software, Inc.

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the Apache 2.0 License. 
#  This program is distributed WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  @author VolumeFi, Software Inc.
#  @notice This Vyper contract adds liquidity to any Uniswap V3 pool using ETH or any ERC20 Token.
#  SPDX-License-Identifier: Apache-2.0

# @version ^0.2.12

struct MintParams:
    token0: address
    token1: address
    fee: uint256
    tickLower: int128
    tickUpper: int128
    amount0Desired: uint256
    amount1Desired: uint256
    amount0Min: uint256
    amount1Min: uint256
    recipient: address
    deadline: uint256

struct SingleMintParams:
    token0: address
    token1: address
    fee: uint256
    tickLower: int128
    tickUpper: int128
    sqrtPriceAX96: uint256
    sqrtPriceBX96: uint256
    liquidityMin: uint256
    recipient: address
    deadline: uint256

struct ModifyParams:
    fee: uint256
    tickLower: int128
    tickUpper: int128
    recipient: address
    deadline: uint256

interface ERC20:
    def balanceOf(_owner: address) -> uint256: view

interface NonfungiblePositionManager:
    def burn(tokenId: uint256): payable

interface WrappedEth:
    def deposit(): payable
    def withdraw(amount: uint256): nonpayable

event AddedLiquidity:
    tokenId: indexed(uint256)
    token0: indexed(address)
    token1: indexed(address)
    liquidity: uint256
    amount0: uint256
    amount1: uint256

event NFLPModified:
    oldTokenId: indexed(uint256)
    newTokenId: indexed(uint256)

event Paused:
    paused: bool

event FeeChanged:
    newFee: uint256

NONFUNGIBLEPOSITIONMANAGER: constant(address) = 0xC36442b4a4522E871399CD717aBDD847Ab11FE88
UNISWAPV3FACTORY: constant(address) = 0x1F98431c8aD98523631AE4a59f267346ea31F984

SWAPROUTER: constant(address) = 0xE592427A0AEce92De3Edee1F18E0157C05861564

VETH: constant(address) = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
WETH: constant(address) = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2

APPROVE_MID: constant(Bytes[4]) = method_id("approve(address,uint256)")
TRANSFER_MID: constant(Bytes[4]) = method_id("transfer(address,uint256)")
TRANSFERFROM_MID: constant(Bytes[4]) = method_id("transferFrom(address,address,uint256)")
CAIPIN_MID: constant(Bytes[4]) = method_id("createAndInitializePoolIfNecessary(address,address,uint24,uint160)")
GETPOOL_MID: constant(Bytes[4]) = method_id("getPool(address,address,uint24)")
SLOT0_MID: constant(Bytes[4]) = method_id("slot0()")
MINT_MID: constant(Bytes[4]) = method_id("mint((address,address,uint24,int24,int24,uint256,uint256,uint256,uint256,address,uint256))")
POSITIONS_MID: constant(Bytes[4]) = method_id("positions(uint256)")
INCREASELIQUIDITY_MID: constant(Bytes[4]) = method_id("increaseLiquidity((uint256,uint256,uint256,uint256,uint256,uint256))")
DECREASELIQUIDITY_MID: constant(Bytes[4]) = method_id("decreaseLiquidity((uint256,uint128,uint256,uint256,uint256))")
COLLECT_MID: constant(Bytes[4]) = method_id("collect((uint256,address,uint128,uint128))")
EIS_MID: constant(Bytes[4]) = method_id("exactInputSingle((address,address,uint24,address,uint256,uint256,uint256,uint160))")

paused: public(bool)
admin: public(address)
feeAddress: public(address)
feeAmount: public(uint256)

@external
def __init__():
    self.paused = False
    self.admin = msg.sender
    self.feeAddress = 0xf29399fB3311082d9F8e62b988cBA44a5a98ebeD
    self.feeAmount = 5 * 10 ** 15

@internal
@pure
def uintSqrt(x: uint256) -> uint256:
    if x > 3:
        z: uint256 = (x + 1) / 2
        y: uint256 = x
        for i in range(256):
            if y == z:
                return y
            y = z
            z = (x / z + z) / 2
        raise "Did not coverage"
    elif x == 0:
        return 0
    else:
        return 1

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
def addLiquidity(_tokenId: uint256, sender: address, uniV3Params: MintParams, _sqrtPriceX96: uint256 = 0) -> (uint256, uint256, uint256):
    self.safeApprove(uniV3Params.token0, NONFUNGIBLEPOSITIONMANAGER, uniV3Params.amount0Desired)
    self.safeApprove(uniV3Params.token1, NONFUNGIBLEPOSITIONMANAGER, uniV3Params.amount1Desired)
    if _tokenId == 0:
        sqrtPriceX96: uint256 = _sqrtPriceX96
        _response32: Bytes[32] = empty(Bytes[32])
        if sqrtPriceX96 == 0:
            _response32 = raw_call(
                UNISWAPV3FACTORY,
                concat(
                    GETPOOL_MID,
                    convert(uniV3Params.token0, bytes32),
                    convert(uniV3Params.token1, bytes32),
                    convert(uniV3Params.fee, bytes32)
                ),
                max_outsize=32,
                is_static_call=True
            )
            pool: address = convert(convert(_response32, bytes32), address)
            assert pool != ZERO_ADDRESS, "Pool does not exist"
            _response224: Bytes[224] = raw_call(
                pool,
                SLOT0_MID,
                max_outsize=224,
                is_static_call=True
            )
            sqrtPriceX96 = convert(slice(_response224, 0, 32), uint256)
            assert sqrtPriceX96 != 0, "Pool does not initialized"

        _response32 = raw_call(
            NONFUNGIBLEPOSITIONMANAGER,
            concat(
                CAIPIN_MID,
                convert(uniV3Params.token0, bytes32),
                convert(uniV3Params.token1, bytes32),
                convert(uniV3Params.fee, bytes32),
                convert(sqrtPriceX96, bytes32)
            ),
            max_outsize=32
        )
        assert convert(convert(_response32, bytes32), address) != ZERO_ADDRESS, "Create Or Init Pool failed"
        _response128: Bytes[128] = raw_call(
            NONFUNGIBLEPOSITIONMANAGER,
            concat(
                MINT_MID,
                convert(uniV3Params.token0, bytes32),
                convert(uniV3Params.token1, bytes32),
                convert(uniV3Params.fee, bytes32),
                convert(uniV3Params.tickLower, bytes32),
                convert(uniV3Params.tickUpper, bytes32),
                convert(uniV3Params.amount0Desired, bytes32),
                convert(uniV3Params.amount1Desired, bytes32),
                convert(uniV3Params.amount0Min, bytes32),
                convert(uniV3Params.amount1Min, bytes32),
                convert(uniV3Params.recipient, bytes32),
                convert(uniV3Params.deadline, bytes32)
            ),
            max_outsize=128
        )
        tokenId: uint256 = convert(slice(_response128, 0, 32), uint256)
        liquidity: uint256 = convert(slice(_response128, 32, 32), uint256)
        amount0: uint256 = convert(slice(_response128, 64, 32), uint256)
        amount1: uint256 = convert(slice(_response128, 96, 32), uint256)
        log AddedLiquidity(tokenId, uniV3Params.token0, uniV3Params.token1, liquidity, amount0, amount1)
        return (amount0, amount1, liquidity)
    else:
        liquidity: uint256 = 0
        amount0: uint256 = 0
        amount1: uint256 = 0
        _response96: Bytes[96] = raw_call(
            NONFUNGIBLEPOSITIONMANAGER,
            concat(
                INCREASELIQUIDITY_MID,
                convert(_tokenId, bytes32),
                convert(uniV3Params.amount0Desired, bytes32),
                convert(uniV3Params.amount1Desired, bytes32),
                convert(uniV3Params.amount0Min, bytes32),
                convert(uniV3Params.amount1Min, bytes32),
                convert(uniV3Params.deadline, bytes32)
            ),
            max_outsize=96
        )
        liquidity = convert(slice(_response96, 0, 32), uint256)
        amount0 = convert(slice(_response96, 32, 32), uint256)
        amount1 = convert(slice(_response96, 64, 32), uint256)
        log AddedLiquidity(_tokenId, uniV3Params.token0, uniV3Params.token1, liquidity, amount0, amount1)
        return (amount0, amount1, liquidity)

@external
@payable
@nonreentrant('lock')
def addLiquidityEthForUniV3(_tokenId: uint256, uniV3Params: MintParams):
    assert not self.paused, "Paused"
    assert convert(uniV3Params.token0, uint256) < convert(uniV3Params.token1, uint256), "Unsorted tokens"
    if uniV3Params.token0 == WETH:
        if msg.value > uniV3Params.amount0Desired:
            send(msg.sender, msg.value - uniV3Params.amount0Desired)
        else:
            assert msg.value == uniV3Params.amount0Desired, "Eth not enough"
        WrappedEth(WETH).deposit(value=uniV3Params.amount0Desired)
        self.safeTransferFrom(uniV3Params.token1, msg.sender, self, uniV3Params.amount1Desired)
        amount0: uint256 = 0
        amount1: uint256 = 0
        liquidity: uint256 = 0
        (amount0, amount1, liquidity) = self.addLiquidity(_tokenId, msg.sender, uniV3Params)
        amount0 = uniV3Params.amount0Desired - amount0
        amount1 = uniV3Params.amount1Desired - amount1
        if amount0 > 0:
            WrappedEth(WETH).withdraw(amount0)
            send(msg.sender, amount0)
            self.safeApprove(uniV3Params.token0, NONFUNGIBLEPOSITIONMANAGER, 0)
        if amount1 > 0:
            self.safeTransfer(uniV3Params.token1, msg.sender, amount1)
            self.safeApprove(uniV3Params.token1, NONFUNGIBLEPOSITIONMANAGER, 0)
    else:
        assert uniV3Params.token1 == WETH, "Not Eth Pair"
        if msg.value > uniV3Params.amount1Desired:
            send(msg.sender, msg.value - uniV3Params.amount1Desired)
        else:
            assert msg.value == uniV3Params.amount1Desired, "Eth not enough"
        WrappedEth(WETH).deposit(value=uniV3Params.amount1Desired)
        self.safeTransferFrom(uniV3Params.token0, msg.sender, self, uniV3Params.amount0Desired)
        amount0: uint256 = 0
        amount1: uint256 = 0
        liquidity: uint256 = 0
        (amount0, amount1, liquidity) = self.addLiquidity(_tokenId, msg.sender, uniV3Params)
        amount0 = uniV3Params.amount0Desired - amount0
        amount1 = uniV3Params.amount1Desired - amount1
        if amount0 > 0:
            self.safeTransfer(uniV3Params.token0, msg.sender, amount0)
            self.safeApprove(uniV3Params.token0, NONFUNGIBLEPOSITIONMANAGER, 0)
        if amount1 > 0:
            WrappedEth(WETH).withdraw(amount1)
            send(msg.sender, amount1)
            self.safeApprove(uniV3Params.token1, NONFUNGIBLEPOSITIONMANAGER, 0)

@external
@nonreentrant('lock')
def addLiquidityForUniV3(_tokenId: uint256, uniV3Params: MintParams):
    assert not self.paused, "Paused"
    assert convert(uniV3Params.token0, uint256) < convert(uniV3Params.token1, uint256), "Unsorted tokens"

    self.safeTransferFrom(uniV3Params.token0, msg.sender, self, uniV3Params.amount0Desired)
    self.safeTransferFrom(uniV3Params.token1, msg.sender, self, uniV3Params.amount1Desired)

    amount0: uint256 = 0
    amount1: uint256 = 0
    liquidity: uint256 = 0
    (amount0, amount1, liquidity) = self.addLiquidity(_tokenId, msg.sender, uniV3Params)
    amount0 = uniV3Params.amount0Desired - amount0
    amount1 = uniV3Params.amount1Desired - amount1
    if amount0 > 0:
        self.safeTransfer(uniV3Params.token0, msg.sender, amount0)
        self.safeApprove(uniV3Params.token0, NONFUNGIBLEPOSITIONMANAGER, 0)
    if amount1 > 0:
        self.safeTransfer(uniV3Params.token1, msg.sender, amount1)
        self.safeApprove(uniV3Params.token1, NONFUNGIBLEPOSITIONMANAGER, 0)

@external
@payable
@nonreentrant('lock')
def modifyPositionForUniV3NFLP(_tokenId: uint256, modifyParams: ModifyParams):
    assert _tokenId != 0, "Wrong Token ID"
    fee: uint256 = self.feeAmount
    if msg.value > fee:
        send(msg.sender, msg.value - fee)
    else:
        assert msg.value == fee, "Insufficient fee"
    send(self.feeAddress, fee)
    
    _response384: Bytes[384] = raw_call(
        NONFUNGIBLEPOSITIONMANAGER,
        concat(
            POSITIONS_MID,
            convert(_tokenId, bytes32)
        ),
        max_outsize=384,
        is_static_call=True
    )
    token0: address = convert(convert(slice(_response384, 64, 32), uint256), address)
    token1: address = convert(convert(slice(_response384, 96, 32), uint256), address)
    liquidity: uint256 = convert(slice(_response384, 224, 32), uint256)
    
    _response64: Bytes[64] = raw_call(
        NONFUNGIBLEPOSITIONMANAGER,
        concat(
            DECREASELIQUIDITY_MID,
            convert(_tokenId, bytes32),
            convert(liquidity, bytes32),
            convert(0, bytes32),
            convert(0, bytes32),
            convert(modifyParams.deadline, bytes32)
        ),
        max_outsize=64
    )

    _response64 = raw_call(
        NONFUNGIBLEPOSITIONMANAGER,
        concat(
            COLLECT_MID,
            convert(_tokenId, bytes32),
            convert(self, bytes32),
            convert(2 ** 128 - 1, bytes32),
            convert(2 ** 128 - 1, bytes32)
        ),
        max_outsize=64
    )
    amount0: uint256 = convert(slice(_response64, 0, 32), uint256)
    amount1: uint256 = convert(slice(_response64, 32, 32), uint256)
    
    NonfungiblePositionManager(NONFUNGIBLEPOSITIONMANAGER).burn(_tokenId)

    sqrtPriceX96: uint256 = 0
    _response32: Bytes[32] = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(token0, bytes32),
            convert(token1, bytes32),
            convert(modifyParams.fee, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool: address = convert(convert(_response32, bytes32), address)
    if pool == ZERO_ADDRESS:
        sqrtPriceX96 = 2 ** 96 * self.uintSqrt(amount0) / self.uintSqrt(amount1)
    else:
        _response224: Bytes[224] = raw_call(
            pool,
            SLOT0_MID,
            max_outsize=224,
            is_static_call=True
        )
        sqrtPriceX96 = convert(slice(_response224, 0, 32), uint256)
        if sqrtPriceX96 == 0:
            sqrtPriceX96 = 2 ** 96 * self.uintSqrt(amount0) / self.uintSqrt(amount1)

    _response32 = raw_call(
        NONFUNGIBLEPOSITIONMANAGER,
        concat(
            CAIPIN_MID,
            convert(token0, bytes32),
            convert(token1, bytes32),
            convert(modifyParams.fee, bytes32),
            convert(sqrtPriceX96, bytes32)
        ),
        max_outsize=32
    )

    assert convert(convert(_response32, bytes32), address) != ZERO_ADDRESS, "Create Or Init Pool failed"

    self.safeApprove(token0, NONFUNGIBLEPOSITIONMANAGER, amount0)
    self.safeApprove(token1, NONFUNGIBLEPOSITIONMANAGER, amount1)

    _response128: Bytes[128] = raw_call(
        NONFUNGIBLEPOSITIONMANAGER,
        concat(
            MINT_MID,
            convert(token0, bytes32),
            convert(token1, bytes32),
            convert(modifyParams.fee, bytes32),
            convert(modifyParams.tickLower, bytes32),
            convert(modifyParams.tickUpper, bytes32),
            convert(amount0, bytes32),
            convert(amount1, bytes32),
            convert(0, bytes32),
            convert(0, bytes32),
            convert(msg.sender, bytes32),
            convert(modifyParams.deadline, bytes32)
        ),
        max_outsize=128
    )
    tokenId: uint256 = convert(slice(_response128, 0, 32), uint256)
    liquiditynew: uint256 = convert(slice(_response128, 32, 32), uint256)
    amount0new: uint256 = convert(slice(_response128, 64, 32), uint256)
    amount1new: uint256 = convert(slice(_response128, 96, 32), uint256)

    if amount0 > amount0new:
        self.safeTransfer(token0, msg.sender, amount0 - amount0new)
        self.safeApprove(token0, NONFUNGIBLEPOSITIONMANAGER, 0)
    if amount1 > amount1new:
        self.safeTransfer(token1, msg.sender, amount1 - amount1new)
        self.safeApprove(token1, NONFUNGIBLEPOSITIONMANAGER, 0)
    log NFLPModified(_tokenId, tokenId)

@internal
def _getMaxFeeLevel(fromToken: address, toToken: address) -> uint256:
    maxFee: uint256 = 0
    _response: Bytes[32] = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(fromToken, bytes32),
            convert(toToken, bytes32),
            convert(500, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool_500: address = convert(convert(_response, bytes32), address)
    bal_500: uint256 = 0
    if pool_500 != ZERO_ADDRESS:
        maxFee = 500
        bal_500 = ERC20(toToken).balanceOf(pool_500)
    _response = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(fromToken, bytes32),
            convert(toToken, bytes32),
            convert(3000, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool_3000: address = convert(convert(_response, bytes32), address)
    bal_3000: uint256 = 0
    if pool_3000 != ZERO_ADDRESS:
        bal_3000 = ERC20(toToken).balanceOf(pool_500)
        if maxFee == 0 or bal_3000 > bal_500:
            maxFee = 3000
    _response = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(fromToken, bytes32),
            convert(toToken, bytes32),
            convert(10000, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool_10000: address = convert(convert(_response, bytes32), address)
    bal_10000: uint256 = 0
    if pool_10000 != ZERO_ADDRESS:
        bal_10000 = ERC20(fromToken).balanceOf(pool_10000)
        if maxFee == 0 or (bal_10000 > bal_3000 and bal_10000 > bal_500):
            maxFee = 10000
    assert maxFee != 0
    return maxFee

@internal
def _token2Token(fromToken: address, toToken: address, feeLevel: uint256, tokens2Trade: uint256, deadline: uint256) -> uint256:
    if fromToken == toToken:
        return tokens2Trade
    self.safeApprove(fromToken, SWAPROUTER, tokens2Trade)
    _response: Bytes[32] = raw_call(
        SWAPROUTER,
        concat(
            EIS_MID,
            convert(fromToken, bytes32),
            convert(toToken, bytes32),
            convert(feeLevel, bytes32),
            convert(self, bytes32),
            convert(deadline, bytes32),
            convert(tokens2Trade, bytes32),
            convert(0, bytes32),
            convert(0, bytes32)
        ),
        max_outsize=32
    )
    tokenBought: uint256 = convert(_response, uint256)
    self.safeApprove(fromToken, SWAPROUTER, 0)
    assert tokenBought > 0, "Error Swapping Token"
    return tokenBought

@internal
@pure
def _getUserInForSqrtPriceX96(sqrtPriceAX96: uint256, sqrtPriceBX96: uint256, sqrtPriceX96: uint256, toInvest: uint256) -> uint256:
    if sqrtPriceBX96 > sqrtPriceAX96:
        return toInvest * sqrtPriceBX96 / (sqrtPriceX96 * (sqrtPriceBX96 - sqrtPriceX96) / (sqrtPriceX96 - sqrtPriceAX96) + sqrtPriceBX96)
    else:
        return toInvest * sqrtPriceX96 / (sqrtPriceX96 + sqrtPriceAX96 * (sqrtPriceX96 - sqrtPriceBX96) / (sqrtPriceAX96 - sqrtPriceX96))

@internal
@view
def _getMidToken(midToken: address, token0: address, token1: address) -> (address, uint256):
    amount0: uint256 = 0
    fee0: uint256 = 500
    _response: Bytes[32] = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(midToken, bytes32),
            convert(token0, bytes32),
            convert(500, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool_500: address = convert(convert(_response, bytes32), address)
    if pool_500 != ZERO_ADDRESS:
        amount0 = ERC20(midToken).balanceOf(pool_500)
    _response = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(midToken, bytes32),
            convert(token0, bytes32),
            convert(3000, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool_3000: address = convert(convert(_response, bytes32), address)
    if pool_3000 != ZERO_ADDRESS:
        amount: uint256 = ERC20(midToken).balanceOf(pool_3000)
        if amount > amount0:
            amount0 = amount
            fee0 = 3000
    _response = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(midToken, bytes32),
            convert(token0, bytes32),
            convert(10000, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool_10000: address = convert(convert(_response, bytes32), address)
    if pool_10000 != ZERO_ADDRESS:
        amount: uint256 = ERC20(midToken).balanceOf(pool_3000)
        if amount > amount0:
            amount0 = amount
            fee0 = 10000

    amount1: uint256 = 0
    fee1: uint256 = 500
    _response = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(midToken, bytes32),
            convert(token1, bytes32),
            convert(500, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool_500 = convert(convert(_response, bytes32), address)
    if pool_500 != ZERO_ADDRESS:
        amount1 = ERC20(midToken).balanceOf(pool_500)
    _response = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(midToken, bytes32),
            convert(token1, bytes32),
            convert(3000, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool_3000 = convert(convert(_response, bytes32), address)
    if pool_3000 != ZERO_ADDRESS:
        amount: uint256 = ERC20(midToken).balanceOf(pool_3000)
        if amount > amount1:
            amount1 = amount
            fee1 = 3000
    _response = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(midToken, bytes32),
            convert(token1, bytes32),
            convert(10000, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool_10000 = convert(convert(_response, bytes32), address)
    if pool_10000 != ZERO_ADDRESS:
        amount: uint256 = ERC20(midToken).balanceOf(pool_10000)
        if amount > amount1:
            amount1 = amount
            fee1 = 10000
    if amount0 > amount1:
        return (token0, fee0)
    else:
        return (token1, fee1)

@external
@payable
@nonreentrant('lock')
def investTokenForUniPair(_token: address, amount: uint256, _tokenId: uint256, _uniV3Params: SingleMintParams):
    assert not self.paused, "Paused"
    assert amount > 0, "Invalid input amount"
    uniV3Params: MintParams = MintParams({
        token0: _uniV3Params.token0,
        token1: _uniV3Params.token1,
        fee: _uniV3Params.fee,
        tickLower: _uniV3Params.tickLower,
        tickUpper: _uniV3Params.tickUpper,
        amount0Desired: 0,
        amount1Desired: 0,
        amount0Min: 0,
        amount1Min: 0,
        recipient: _uniV3Params.recipient,
        deadline: _uniV3Params.deadline
    })
    assert convert(uniV3Params.token0, uint256) < convert(uniV3Params.token1, uint256), "Unsorted tokens"
    fee: uint256 = self.feeAmount
    assert msg.value >= fee, "Insufficient fee"
    send(self.feeAddress, fee)
    msg_value: uint256 = msg.value
    msg_value -= fee
    token: address = _token
    _response32: Bytes[32] = empty(Bytes[32])
    toInvest: uint256 = 0
    midToken: address = WETH
    if token == VETH or token == ZERO_ADDRESS:
        if msg_value > amount:
            send(msg.sender, msg_value - amount)
        else:
            assert msg_value >= amount, "Insufficient value"
        WrappedEth(WETH).deposit(value=amount)
        token = WETH
        toInvest = amount
    #invest Token
    else:
        self.safeTransferFrom(token, msg.sender, self, amount)
        if msg_value > 0:
            send(msg.sender, msg_value)
        if token == WETH:
            toInvest = amount
        elif token != uniV3Params.token0 and token != uniV3Params.token1:
            maxFeeLevel:uint256 = self._getMaxFeeLevel(token, WETH)
            toInvest = self._token2Token(token, WETH, maxFeeLevel, amount, uniV3Params.deadline)
        else:
            midToken = token
            toInvest = amount
    if uniV3Params.token0 != WETH and uniV3Params.token1 != WETH and token != uniV3Params.token0 and token != uniV3Params.token1:
        maxFeeLevel:uint256 = 0
        (midToken, maxFeeLevel) = self._getMidToken(WETH, uniV3Params.token0, uniV3Params.token1)
        toInvest = self._token2Token(WETH, midToken, maxFeeLevel, toInvest, uniV3Params.deadline)

    endToken: address = ZERO_ADDRESS
    if midToken == uniV3Params.token0:
        endToken = uniV3Params.token1
    else:
        endToken = uniV3Params.token0

    sqrtPriceX96: uint256 = 0
    _response32 = raw_call(
        UNISWAPV3FACTORY,
        concat(
            GETPOOL_MID,
            convert(uniV3Params.token0, bytes32),
            convert(uniV3Params.token1, bytes32),
            convert(uniV3Params.fee, bytes32)
        ),
        max_outsize=32,
        is_static_call=True
    )
    pool: address = convert(convert(_response32, bytes32), address)
    assert pool != ZERO_ADDRESS, "Pool does not exist"
    _response224: Bytes[224] = raw_call(
        pool,
        SLOT0_MID,
        max_outsize=224,
        is_static_call=True
    )
    sqrtPriceX96 = convert(slice(_response224, 0, 32), uint256)
    assert sqrtPriceX96 != 0, "Pool does not initialized"
    retAmount: uint256 = 0
    swapAmount: uint256 = 0
    if sqrtPriceX96 <= _uniV3Params.sqrtPriceAX96:
        if convert(midToken, uint256) > convert(endToken, uint256):
            swapAmount = toInvest
    elif sqrtPriceX96 >= _uniV3Params.sqrtPriceBX96:
        if convert(midToken, uint256) < convert(endToken, uint256):
            swapAmount = toInvest
    else:
        if convert(midToken, uint256) < convert(endToken, uint256):
            swapAmount = self._getUserInForSqrtPriceX96(_uniV3Params.sqrtPriceAX96, _uniV3Params.sqrtPriceBX96, sqrtPriceX96, toInvest)
        else:
            swapAmount = self._getUserInForSqrtPriceX96(_uniV3Params.sqrtPriceBX96, _uniV3Params.sqrtPriceAX96, sqrtPriceX96, toInvest)

    if swapAmount > toInvest:
        swapAmount = toInvest

    if swapAmount > 0:
        retAmount = self._token2Token(midToken, endToken, uniV3Params.fee, swapAmount, uniV3Params.deadline)

    if uniV3Params.token0 == midToken:
        uniV3Params.amount0Desired = toInvest - swapAmount
        uniV3Params.amount1Desired = retAmount
    else:
        uniV3Params.amount1Desired = toInvest - swapAmount
        uniV3Params.amount0Desired = retAmount

    amount0: uint256 = 0
    amount1: uint256 = 0
    liquidity: uint256 = 0
    (amount0, amount1, liquidity) = self.addLiquidity(_tokenId, msg.sender, uniV3Params, sqrtPriceX96)
    assert liquidity >= _uniV3Params.liquidityMin, "High Slippage"
    amount0 = uniV3Params.amount0Desired - amount0
    amount1 = uniV3Params.amount1Desired - amount1
    if amount0 > 0:
        self.safeTransfer(uniV3Params.token0, msg.sender, amount0)
        self.safeApprove(uniV3Params.token0, NONFUNGIBLEPOSITIONMANAGER, 0)
    if amount1 > 0:
        self.safeTransfer(uniV3Params.token1, msg.sender, amount1)
        self.safeApprove(uniV3Params.token1, NONFUNGIBLEPOSITIONMANAGER, 0)

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
            self.safeTransfer(token[i], to[i], amount[i])

@external
@nonreentrant('lock')
def withdraw(token: address, amount: uint256, to: address):
    assert msg.sender == self.admin, "Not admin"
    if token == VETH:
        send(to, amount)
    elif token != ZERO_ADDRESS:
        self.safeTransfer(token, to, amount)

@external
@payable
def __default__():
    assert msg.sender == WETH, "can't receive Eth"