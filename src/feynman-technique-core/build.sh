dos2unix docker-compose.yml
dos2unix Dockerfile

chmod +x docker-compose.yml
chmod +x Dockerfile

echo "> Composing application..."
docker compose up -d
echo "> Finish!"