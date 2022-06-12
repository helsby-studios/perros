#!/bin/bash
git clone https://github.com/helsby-studios/perros.git perros
cd perros || exit
chmod +x dockerized.sh
sudo ./dockerized.sh