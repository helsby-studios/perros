This is the Rewrite Branch, proceed with caution!
# PerrOS
PerrOS is a Opensource Discord Bot to do it all!  
[![Super-Linter](https://github.com/cloud-corp/perros/actions/workflows/super-linter.yml/badge.svg)](https://github.com/cloud-corp/perros/actions/workflows/super-linter.yml)  
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/download/server/)
[![Discord](https://img.shields.io/badge/%3CPerros%3E-%237289DA.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/pZKPM5kWyk)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

## Installation

### Manual installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the python3 requirements.

```bash
pip3 install -r requirements.txt --no-deps
```
Then run main.py.
```bash
python3 main.py
```
Go to the IP adress show in the Console and finish the Web-Setup.
More information can be found in our [wiki](https://github.com/cloud-corp/perros/wiki).

<sub>Note that PerrOS is designed to work on Linux especially Ubuntu Server, it might work any other os too but its not recomended</sup>

### Dockerized installation
Install PerrOS in a docker container.
#### Automated
To perform an automated install (recommended for beginners) you can use the following commands:
```bash
chmod +x dockerized.sh
sudo ./dockerized.sh
````
After editing the config file you can enjoy PerrOS on port 80 and finish the [web](127.0.0.1) setup.

To uninstall PerrOS you can use the following commands:
```bash
chmod +x ./uninstall-dockerized.sh
sudo ./uninstall-dockerized.sh
````
#### Manual
To perform a manual install you can use the following commands:
```bash
docker build -t perros .
docker run -p 80:80 -v perros-data:/app -d perros
```
Alternative commands:
```bash
docker build -t perros .
docker run --network="host" -p 80:80 -v /path/to/folder:/app -d perros
```

To uninstall PerrOS you can use the following commands:
```bash
docker stop perros
docker rm -f perros
docker volume remove prerros-data
````

## Usage
To dump the Volumes of PerrOS you can use the following commands:
```bash
docker cp perros:/app .
docker cp . perros:/app
```

Coming Soon

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

For more detailed guidelines please read our [wiki](https://github.com/helsby-studios/perros/wiki/Contributing)

## License
PerrOS is licensed under
[GPLV3](https://choosealicense.com/licenses/gpl-3.0/)


If anyone is crazy enough to donate to a random developer in Europe, heres my ETH address:
0x1Eb4317add0E70873A88F36987b0003d8830D87D
