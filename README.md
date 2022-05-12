# PerrOS
PerrOS is a Opensource Discord Bot to do it all!


## Installation

### Manual installation:
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

### Dockerized installation:
Install PerrOS in a docker container.
#### Automated:
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
#### Manual:
To perform a manual install you can use the following commands:
```bash
docker build -t perros .
docker run perros -p 80:80 -v perros-data:/app -d
````
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
```

Coming Soon

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
PerrOS is licensed under
[GPLV3](https://choosealicense.com/licenses/gpl-3.0/)
