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


def mine(blocks):
    get_connection().generate(blocks)


def send_coins(address, amount):
    get_connection().sendtoaddress(address, amount)


if __name__ == '__main__':
    mine(101)
