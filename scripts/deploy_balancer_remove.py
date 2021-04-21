from brownie import BalancerExchangeRemove, accounts

def main():
    acct = accounts.load("deployer_account")
    # BalancerExchangeRemove.deploy({"from":acct, "gasPrice":100 * 10 ** 9})
    BalancerExchangeRemove.deploy({"from":acct})