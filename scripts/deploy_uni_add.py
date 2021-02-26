from brownie import UniswapExchangeAdd, accounts

def main():
    acct = accounts.load("deployer_account")
    # UniswapExchangeAdd.deploy({"from":acct, "gasPrice":100 * 10 ** 9})
    UniswapExchangeAdd.deploy({"from":acct})