user    := "atareao"
name    := `basename ${PWD}`
version := `git tag -l  | tail -n1`

rebuild:
    echo {{version}}
    echo {{name}}
    docker build --no-cache \
                 -t {{user}}/{{name}}:{{version}} \
                 -t {{user}}/{{name}}:latest \
                 .
build:
    echo {{version}}
    echo {{name}}
    docker build -t {{user}}/{{name}}:{{version}} \
                 -t {{user}}/{{name}}:latest \
                 .

push:
    docker push {{user}}/{{name}}:{{version}}
    docker push {{user}}/{{name}}:latest

start:
    docker run --rm \
               --init \
               --name {{name}} \
               --detach \
               --env-file .env \
               {{user}}/{{name}}:latest

logs:
    docker logs {{name}} -f

stop:
    docker stop {{name}}

exec:
    docker run --rm \
               -it \
               --init \
               --name {{name}} \
               --env-file .env \
               {{user}}/{{name}}:latest \
               sh

run:
    poetry run python src/main.py

test:
    poetry run pytest tests/*
