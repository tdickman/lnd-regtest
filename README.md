This is a collection of scripts and docker images that can be used to run
bitcoind and an arbitrary number of lnd instances in a regtest configuration.
It uses docker-compose + some custom python scripts to create the specified
number of lnd instances, and connect them via the channel configuration
specified in `config.yaml`.

# Requirements

* docker
* docker-compose
* python 3.6
* pipenv

# Usage

Setup environment:

```
cp config.TEMPLATE.yaml config.yaml
pipenv shell
pipenv install
```

Start bitcoind, lnd instances, and setup all specified channels

```
python start.py
```

Stop everything:

```
python stop.py
```

# Configuration

Modify `config.yaml` to setup your desired network and rerun `start.py` to
update the network.
