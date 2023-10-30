FROM ubuntu:22.04 AS basic

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /var/magdalena

WORKDIR /var/magdalena

COPY requirements.txt ./

RUN python3 -m pip install \
    --requirement requirements.txt \
    --no-cache-dir \
    --progress-bar off \
    --no-input \
    --no-color \
    && rm requirements.txt

CMD flask run --host 0.0.0.0 --port 5000 --reload --debug --debugger

EXPOSE 5000

FROM basic AS dev

COPY requirements.dev.txt ./

RUN python3 -m pip install \
    --requirement requirements.dev.txt \
    --no-cache-dir \
    --progress-bar off \
    --no-input \
    --no-color \
    && rm requirements.dev.txt

FROM dev AS prod

COPY LICENSE README.md app.py methodshub.py templates ./

CMD flask run --host 0.0.0.0 --port 5000 --no-reload  --no-debug --no-debugger
