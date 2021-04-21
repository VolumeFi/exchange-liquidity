from brownie import BalancerExchangeAdd, accounts

def main():
    acct = accounts.load("deployer_account")
    # BalancerExchangeAdd.deploy({"from":acct, "gasPrice":100 * 10 ** 9})
    BalancerExchangeAdd.deploy({"from":acct})