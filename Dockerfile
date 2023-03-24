#Eigenentwicklung
FROM python:latest

RUN useradd xenivcdi

WORKDIR /home/xenivcdi

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY xenivcdi.py config.py boot.sh ./
COPY wsgi.py wsgi.py
RUN chmod a+x boot.sh

ENV FLASK_APP xenivcdi.py

RUN chown -R xenivcdi:xenivcdi ./
USER xenivcdi

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
