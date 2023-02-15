FROM continuumio/miniconda3

RUN conda install -c conda-forge tensorflow -y
RUN conda install -c huggingface transformers -y
RUN conda install -c pytorch pytorch -y
RUN conda install -c anaconda pillow -y


COPY resources/startup.sh /usr/local/bin/startup.sh
COPY resources/requirements.txt /usr/local/requirements.txt
RUN python3 -m pip install -r /usr/local/requirements.txt
RUN chmod 777 /usr/local/bin/startup.sh

WORKDIR /app
VOLUME ["/app"]


EXPOSE 8001
CMD ["sh", "/usr/local/bin/startup.sh"]