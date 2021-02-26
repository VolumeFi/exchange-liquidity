from brownie import UniswapExchangeRemove, accounts

def main():
    acct = accounts.load("deployer_account")
    # UniswapExchangeRemove.deploy({"from":acct, "gasPrice":100 * 10 ** 9})
    UniswapExchangeRemove.deploy({"from":acct})