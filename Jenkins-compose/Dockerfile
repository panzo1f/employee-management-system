FROM jenkins/jenkins:lts

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

USER jenkins