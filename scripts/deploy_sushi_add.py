from brownie import SushiswapExchangeAdd, accounts

def main():
    acct = accounts.load("deployer_account")
    # SushiswapExchangeAdd.deploy({"from":acct, "gasPrice":100 * 10 ** 9})
    SushiswapExchangeAdd.deploy({"from":acct})