## Run locally
    export FLASK_APP=chordrec
    export TELEGRAM_TOKEN=<token>
    export TELEGRAM_CHAT_ID=<chat_id>
    python -m flask run --port 8080

## Disabling TELEGRAM notifications
    export DEBUG=True

## Run tests
    py.test -s

## Run in docker
    docker build -t odiscort/solfege.dev:latest .
    docker push odiscort/solfege.dev:latest
    docker run --publish 8080:8080 <image_id>