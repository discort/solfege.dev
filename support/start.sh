#!/bin/sh

nginx && uwsgi --http "127.0.0.1:8081" --module "chordrec:create_app()" --processes 2 --threads 4