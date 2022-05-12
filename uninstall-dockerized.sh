#!/usr/bin/bash
echo "Uninstalling perros docker..."
docker-compose down
docker rm -f perros_perros
docker volume remove perros_prerros-data
echo "nukeing files..."
rm -r ./*
echo "uninstalled perros docker..."
echo "bye!"