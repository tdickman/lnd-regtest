import subprocess
import time
import yaml
from jinja2 import Template


def get_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def render_docker_compose(config):
    with open('config/docker-compose.TEMPLATE.yml', 'r') as f:
        template = Template(f.read())
        config['containers'] = ['lnd{}'.format(i) for i in range(config['lnd_instances'])]
        with open('docker-compose.yml', 'w') as f:
            f.write(template.render(**config))


def _run(command):
    subprocess.run(command, shell=True)


def start_docker(config):
    # Cleanup
    _run('docker-compose down --remove-orphans')
    _run('docker-compose rm -f')
    _run('sudo rm -rf data/')

    # Setup config files
    _run('mkdir -p data/')
    _run('mkdir -p data/bitcoind/')
    _run('cp config/bitcoin.conf data/bitcoind/')

    for i in range(config['lnd_instances']):
        _run('mkdir -p data/lnd{}'.format(i))
        _run("sed 's/NAME/lnd{}/g' config/lnd.conf > data/lnd{}/lnd.conf".format(i, i))

    _run('docker-compose build')
    try:
        _run('docker-compose up -d')
        _run('docker-compose exec manager python init.py')
    except KeyboardInterrupt:
        print('Quiting, please wait')
        _run('docker-compose down --remove-orphans')
        # Wait up to 10 seconds for all of our children to die
        time.sleep(10)


if __name__ == '__main__':
    config = get_config()
    render_docker_compose(config)
    start_docker(config)
