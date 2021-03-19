from brownie import CurveExchangeAdd, accounts

def main():
    acct = accounts.load("deployer_account")
    # CurveExchangeAdd.deploy({"from":acct, "gasPrice":100 * 10 ** 9})
    CurveExchangeAdd.deploy({"from":acct})