FROM python:latest
RUN pip install kafka-python
RUN pip install cassandra-driver
RUN pip install datetime
RUN pip install requests
RUN pip install psycopg2-binary
COPY ./read_stream.py /opt/app/
ENTRYPOINT ["python", "/opt/app/read_stream.py"]