from brownie import CurveExchangeRemove, accounts

def main():
    acct = accounts.load("deployer_account")
    # CurveExchangeRemove.deploy({"from":acct, "gasPrice":100 * 10 ** 9})
    CurveExchangeRemove.deploy({"from":acct})