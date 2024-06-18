# Build image
```commandline
docker build -t jenkins:jenkins_04122023 -f jenkins.Dockerfile .
```
# Run Docker Compose
```commandline
docker-compose -f jenkins.docker-compose.yml up -d
```
# Access Service:
```commandline
http://127.0.0.1:8080/
```
# ...
```commandline
docker ps -a
docker exec -it jenkins /bin/bash
docker exec --user root -it jenkins /bin/bash
docker-compose -f jenkins.docker-compose.yml down

```

