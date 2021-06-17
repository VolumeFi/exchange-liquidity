from brownie import UniswapV3ExchangeRemove, accounts

def main():
    acct = accounts.load("deployer_account")
    # UniswapV3ExchangeRemove.deploy({"from":acct, "gasPrice":100 * 10 ** 9})
    UniswapV3ExchangeRemove.deploy({"from":acct})