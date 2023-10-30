FROM ubuntu:22.04 AS dev

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y python3 python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /var/magdalena

WORKDIR /var/magdalena

COPY requirements.txt ./

RUN python3 -m pip install \
    --requirement requirements.txt \
    --no-cache-dir \
    --progress-bar off \
    --no-input \
    --no-color

CMD flask run --host 0.0.0.0 --port 5000 --reload --debug --debugger

EXPOSE 5000

FROM dev AS prod

COPY LICENSE README.md app.py templates ./

CMD flask run --host 0.0.0.0 --port 5000 --no-reload  --no-debug --no-debugger
