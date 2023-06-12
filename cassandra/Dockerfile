FROM python:latest
RUN pip install flask
RUN pip install requests
RUN pip install datetime
RUN pip install cassandra-driver
RUN pip install hazelcast-python-client
COPY ./main.py /opt/app/
ENTRYPOINT ["python", "/opt/app/main.py"]