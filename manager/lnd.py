import codecs, grpc, os
import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc


PASSWORD = "password"


def _macaroon(container):
    return '/mnt/{}/data/chain/bitcoin/regtest/admin.macaroon'.format(container)


def get_channel(container):
    os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
    cert = open('/mnt/{}/tls.cert'.format(container), 'rb').read()
    ssl_creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel('{}:10009'.format(container), ssl_creds)
    return channel


def gen_seed(container):
    channel = get_channel(container)
    stub = lnrpc.WalletUnlockerStub(channel)
    request = ln.GenSeedRequest()
    response = stub.GenSeed(request)
    return response.cipher_seed_mnemonic


def create_wallet(container):
    channel = get_channel(container)
    stub = lnrpc.WalletUnlockerStub(channel)
    request = ln.InitWalletRequest(
        wallet_password=PASSWORD.encode(),
        cipher_seed_mnemonic=gen_seed(container),
    )
    response = stub.InitWallet(request)
    print(response)


def new_address(container):
    channel = get_channel(container)
    macaroon = codecs.encode(open(_macaroon(container), 'rb').read(), 'hex')
    stub = lnrpc.LightningStub(channel)
    request = ln.NewAddressRequest(type=0)
    response = stub.NewAddress(request, metadata=[('macaroon', macaroon)])
    return response.address


def get_info(container):
    channel = get_channel(container)
    macaroon = codecs.encode(open(_macaroon(container), 'rb').read(), 'hex')
    stub = lnrpc.LightningStub(channel)
    request = ln.GetInfoRequest()
    response = stub.GetInfo(request, metadata=[('macaroon', macaroon)])
    return response


def is_synced(container):
    # Macaroons take a bit to mint - assume we aren't synced
    # if they don't exist yet
    if not os.path.exists(_macaroon(container)):
        return False
    return get_info(container).synced_to_chain


def open_channel(source_container, dest_container, amount):
    """Open a channel between the 2 specified containers."""


if __name__ == '__main__':
    create_wallet('lnd1')
