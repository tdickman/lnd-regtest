import itertools
import time
import yaml

import bitcoind
import lnd


def get_config():
    with open('/config.yaml', 'r') as f:
        return yaml.safe_load(f)


LND_COUNT = get_config()['lnd_instances']


def get_container_pairs():
    containers = [i for i in range(LND_COUNT)]
    pairs = list(itertools.product(containers, containers))
    pairs = [p for p in pairs if p[0] != p[1]]
    return pairs


def l(i):
    return 'lnd{}'.format(i)


def wait_until_synced_all():
    # Wait for all containers to fully sync
    for i in range(LND_COUNT):
        wait_until_synced(i)


def wait_until_synced(i):
    try:
        while not lnd.is_synced(l(i)):
            time.sleep(1)
    # Sometimes connection errors occur - need to find a
    # better way to handle these
    except Exception:
        time.sleep(1)


def open_channel(source, destination, amount):
    print('Opening channel from {} to {}'.format(pair[0], pair[1]))
    lnd.open_channel(l(source), l(destination), amount)


if __name__ == '__main__':
    config = get_config()
    premine_blocks = config['premine_blocks']
    bitcoind.mine(premine_blocks)

    for i in range(LND_COUNT):
        print('Creating wallet {}'.format(i))
        lnd.create_wallet(l(i))

    print('Waiting for lnd instances to fully sync')
    wait_until_synced_all()

    for i in range(LND_COUNT):
        address = lnd.new_address(l(i))
        print('Sending coins to wallet {}'.format(i))
        bitcoind.send_coins(address, config['lnd_deposit_btc'])

    bitcoind.mine(5)
    wait_until_synced_all()

    # Open channels
    if config['connect_all']:
        for i, pair in enumerate(get_container_pairs()):
            open_channel(pair[0], pair[1], config['connect_all_amount'])
            if i % 10:
                bitcoind.mine(1)
                wait_until_synced_all()

    for i, channel in enumerate(config['channels']):
        open_channel(channel['from'], channel['to'], channel['amount'])
        if i % 10:
            bitcoind.mine(1)
            wait_until_synced_all()

    bitcoind.mine(6)
