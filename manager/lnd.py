import time
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


def connect(source_container, dest_container):
    dest_info = get_info(dest_container)

    channel = get_channel(source_container)
    macaroon = codecs.encode(open(_macaroon(source_container), 'rb').read(), 'hex')
    stub = lnrpc.LightningStub(channel)
    addr = ln.LightningAddress(
        pubkey=dest_info.identity_pubkey,
        host=dest_container,
    )
    request = ln.ConnectPeerRequest(addr=addr)
    stub.ConnectPeer(request, metadata=[('macaroon', macaroon)])


def open_channel(source_container, dest_container, amount):
    """Open a channel between the 2 specified containers."""

    # source_info = get_info(source_container)
    dest_info = get_info(dest_container)
    try:
        connect(source_container, dest_container)
    except Exception:
        # TODO: Catch more specific error
        pass

    channel = get_channel(source_container)
    macaroon = codecs.encode(open(_macaroon(source_container), 'rb').read(), 'hex')
    stub = lnrpc.LightningStub(channel)
    request = ln.OpenChannelRequest(
        node_pubkey_string=dest_info.identity_pubkey,
        local_funding_amount=amount,
        spend_unconfirmed=True,
    )
    stub.OpenChannelSync(request, metadata=[('macaroon', macaroon)])


def wait_until_synced(container):
    try:
        while not is_synced(container):
            time.sleep(1)
    # Sometimes connection errors occur - need to find a
    # better way to handle these
    except Exception:
        time.sleep(1)


if __name__ == '__main__':
    create_wallet('lnd1')
