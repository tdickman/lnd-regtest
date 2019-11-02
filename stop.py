import subprocess


if __name__ == '__main__':
    subprocess.run('docker-compose down --remove-orphans', shell=True)
