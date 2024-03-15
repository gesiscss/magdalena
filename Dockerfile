FROM ubuntu:22.04 AS basic

WORKDIR /var/magdalena

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get -y install \
    python3 \
    python3-pip \
    git \
    ca-certificates \
    curl \
    gnupg \
    && install -m 0755 -d /etc/apt/keyrings \
    && { curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg ; } \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && { echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu     "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null ; } \
    && apt-get -y update \
    && apt-get -y install \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY poetry.lock ./

RUN python3 -m pip install poetry \
    --no-cache-dir \
    --progress-bar off \
    --no-input \
    --no-color \
    && poetry config virtualenvs.create false \
    && poetry config experimental.new-installer false \
    && poetry install \
    --without dev \
    --no-interaction \
    --no-ansi \
    && pip cache purge

CMD flask run --host 0.0.0.0 --port 5000 --reload --debug --debugger

EXPOSE 5000

FROM basic AS dev

RUN poetry config virtualenvs.create false \
    && poetry config experimental.new-installer false \
    && poetry install \
    --with dev \
    --no-interaction \
    --no-ansi \
    && pip cache purge

FROM basic AS prod

RUN python3 -m pip install \
    gunicorn \
    --no-cache-dir \
    --progress-bar off \
    --no-input \
    --no-color

# COPY source directory itself isn't copied, only its contents.
# See .dockerignore for files that are not copied.
COPY . ./

CMD gunicorn --workers=2 --bind 0.0.0.0:5000 'wsgi:app'
