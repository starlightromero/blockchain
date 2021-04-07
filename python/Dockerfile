FROM python:3.8

LABEL decription="Production image for DeadCoin."

WORKDIR /usr/src/app

COPY python/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY python .

ENV FLASK_APP=node.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
