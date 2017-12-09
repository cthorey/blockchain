kblock() {
    docker run -e ROOT_DIR='/workdir' \
           -v $PWD:/workdir \
           --rm \
           -it \
           -p 80:5000 \
           -p 8888:8888 \
           blockchain jupyter notebook
}
