# BoardManager

Implements the rules of chess, the board and pieces.

# Tests
Tests are run in a [Docker](https://docs.docker.com/engine/install/) container (image created using `test/docker/Dockerfile` based on _python:3.11-slim-bookworm_). 
Developers and automation can run them through the docker-compose (`test/docker/docker-compose.yml`) which contains the relevant configuration:
```commandline
cd PROJECTROOTDIR
docker-compose -f ./test/docker/docker-compose.yml up --build 
```
