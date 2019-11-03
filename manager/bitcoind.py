import time

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

HOSTNAME = 'bitcoind'
USERNAME = 'rpcuser'
PASSWORD = 'rpcpassword'


def get_connection():
    return AuthServiceProxy('http://{}:{}@{}:8332'.format(
        USERNAME,
        PASSWORD,
        HOSTNAME,
    ))


def get_info():
    return get_connection().getblockchaininfo()


def mine(blocks):
    get_connection().generate(blocks)


def send_coins(address, amount):
    get_connection().sendtoaddress(address, amount)


def is_ready():
    try:
        get_info()
    except JSONRPCException as e:
        if e.code != -28:
            raise
        return False

    return True


def wait_until_ready():
    print('Waiting for bitcoind to initialize')
    while not is_ready():
        time.sleep(1)


if __name__ == '__main__':
    mine(101)
