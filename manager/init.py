import time

import bitcoind
import lnd


def l(i):
    return 'lnd{}'.format(i)


if __name__ == '__main__':
    LND_COUNT = 2

    bitcoind.mine(101)

    for i in range(LND_COUNT):
        lnd.create_wallet(l(i))

    # Wait for all containers to fully sync
    for i in range(LND_COUNT):
        try:
            while not lnd.is_synced(l(i)):
                time.sleep(1)
        # Sometimes connection errors occur
        except Exception:
            time.sleep(1)

    for i in range(LND_COUNT):
        address = lnd.new_address(l(i))
        bitcoind.send_coins(address, 10)

    bitcoind.mine(1)

    # Open channels
