FROM python:3.11.9-slim

RUN apt-get update && apt-get install -y \
    vim \
    git

ENV POETRY_VERSION=1.7.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt-get update && apt-get install -y curl --no-install-recommends \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /pitchProject

COPY ${PWD} /pitchProject

RUN chown -R root:root /pitchProject && chmod -R 755 /pitchProject

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
