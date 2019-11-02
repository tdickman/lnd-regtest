import itertools
import time

import bitcoind
import lnd


LND_COUNT = 5


def get_container_pairs():
    containers = [l(i) for i in range(LND_COUNT)]
    pairs = list(itertools.product(containers, containers))
    pairs = [p for p in pairs if p[0] != p[1]]
    return pairs


def l(i):
    return 'lnd{}'.format(i)


def wait_until_synced():
    # Wait for all containers to fully sync
    for i in range(LND_COUNT):
        try:
            while not lnd.is_synced(l(i)):
                time.sleep(1)
        # Sometimes connection errors occur - need to find a
        # better way to handle these
        except Exception:
            time.sleep(1)


if __name__ == '__main__':
    bitcoind.mine(110)

    for i in range(LND_COUNT):
        lnd.create_wallet(l(i))

    wait_until_synced()

    for i in range(LND_COUNT):
        address = lnd.new_address(l(i))
        bitcoind.send_coins(address, 10)

    bitcoind.mine(1)
    wait_until_synced()

    # Open channels
    for pair in get_container_pairs():
        lnd.open_channel(pair[0], pair[1], 1000000)
    bitcoind.mine(6)
