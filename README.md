This is a collection of scripts and docker images that can be used to run
bitcoind and lnd in a regtest configuration.

Mine 101 blocks to get a balance of 50 (coins aren't spendable until 100 blocks have passed):

```
bitcoin-cli generate 101
```
