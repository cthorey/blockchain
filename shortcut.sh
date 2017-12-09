kblock() {
    docker run -e ROOT_DIR='/workdir' \
           -v $PWD:/workdir \
           --rm \
           -e PASSWORD=tf \
           -e ROOT_DIR='/workdir' \
           -it \
           -p 80:5000 \
           -p 8888:8888 \
           blockchain
}

kchain() {
    docker run -e ROOT_DIR='/workdir' \
           -v $PWD:/workdir \
           --rm \
           -e PASSWORD=tf \
           -e PORT=$2 \
           -e ROOT_DIR='/workdir' \
           -p $1:$2 \
           blockchain python app.py
}

