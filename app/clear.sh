docker rmi $(docker images -aq)
docker rm -f $(docker ps -aq)
docker images

echo "sudo docker run -p 8000:8000 "