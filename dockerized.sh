#!/bin/bash
echo "installing docker"
apt update
apt install docker docker-compose -y

echo "setting up config"
cp .env.example .env
nano .env

echo "deploying container"
docker-compose up -d