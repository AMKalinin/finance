FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
# Устанавливаем зависимости для Python и системы
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python 3.12.3 через pyenv (чтобы получить точную версию)
SHELL ["/bin/bash", "-c"]
RUN curl https://pyenv.run | bash && \
    export PATH="$HOME/.pyenv/bin:$PATH" && \
    eval "$(pyenv init --path)" && \
    eval "$(pyenv virtualenv-init -)" && \
    pyenv install 3.12.3 && \
    pyenv global 3.12.3

# Добавляем Python 3.12.3 в PATH
ENV PATH="/root/.pyenv/shims:/root/.pyenv/bin:$PATH"

# Устанавливаем Poetry (менеджер зависимостей)
COPY poetry-install-script.py /tmp/
RUN python3 /tmp/poetry-install-script.py && \
    export PATH="/root/.local/bin:$PATH" && \
	poetry config virtualenvs.create true && \
	rm /tmp/poetry-install-script.py

ENV PATH="/root/.local/bin:/root/.pyenv/shims:/root/.pyenv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . /app

EXPOSE 8001

ENTRYPOINT [ "poetry", "run", "./run.sh" ]
