FROM python:latest
RUN pip install flask
RUN pip install requests
RUN pip install datetime
RUN pip install psycopg2-binary
COPY ./main.py /opt/app/
ENTRYPOINT ["python", "/opt/app/main.py"]