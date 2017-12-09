FROM python:3.6

RUN pip3 install requests flask

RUN pip3 --no-cache-dir install \
        jupyter \
        ipython \
        pandas \
        hashlib

COPY ./run_jupyter.sh /run_jupyter.sh
COPY ./jupyter_notebook_config.py /root/.jupyter/

WORKDIR /workdir

EXPOSE 5000
EXPOSE 8888

CMD ["/run_jupyter.sh", "--allow-root"]

