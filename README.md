# exchange-add
Liquidity Exchange and Add to Pool

## Infura Key
```bash
export WEB3_INFURA_PROJECT_ID=${YOUR_INFURA_KEY}
```

## Add account
```bash
brownie accounts new deployer_account
```

input private key and password


## Test
```bash
brownie test -s
```

## Deployment
```bash
brownie run deploy.py --network mainnet