# Cleanup
docker-compose rm -f
sudo rm -rf data/

# Setup config files
mkdir -p data/
mkdir -p data/bitcoind/
cp bitcoin.conf data/bitcoind/
mkdir -p data/lnd1/
cp lnd.conf data/lnd1/

# Start
docker-compose up
