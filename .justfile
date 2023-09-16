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
    docker push --all-tags {{user}}/{{name}}

run:
    docker run --rm \
               --init \
               --name {{name}} \
               --detach \
               --env-file .env \
               {{user}}/{{name}}:latest


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

test:
    python -m unittest discover -s tests -p "*.py"
