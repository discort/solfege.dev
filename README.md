## Run locally
    export FLASK_APP=chordrec
    python -m flask run --port 8080

## Run tests
    py.test -s

## Run in docker
    docker build .
    docker run --publish 8080:8080 <image_id>