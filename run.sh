# Cleanup
docker-compose rm -f
sudo rm -rf data/

# Setup config files
mkdir -p data/
mkdir -p data/bitcoind/
cp config/bitcoin.conf data/bitcoind/

END=1
for i in $(seq 0 $END); do
    mkdir -p data/lnd$i/;
    sed 's/NAME/lnd'$i'/g' config/lnd.conf > data/lnd$i/lnd.conf;
done;

# Start
docker-compose build
docker-compose up
