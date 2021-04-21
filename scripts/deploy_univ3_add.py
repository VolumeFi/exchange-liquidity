from brownie import UniswapV3ExchangeAdd, accounts

def main():
    acct = accounts.load("deployer_account")
    # UniswapV3ExchangeAdd.deploy({"from":acct, "gasPrice":100 * 10 ** 9})
    UniswapV3ExchangeAdd.deploy({"from":acct})