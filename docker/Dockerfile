FROM python:3.11
RUN  mkdir app
RUN  cd  app
WORKDIR  /app
ADD main.py .
RUN pip install PyYAML
RUN chmod +x main.py

EXPOSE 9

CMD ["python", "-u", "./main.py"]