FROM bcgovimages/von-image:py36-1.16-0 AS base

# Install and Configure Poetry
USER root
ENV POETRY_VERSION=1.1.11
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="/opt/poetry/bin:$PATH"
RUN poetry config virtualenvs.in-project true

# Setup project
WORKDIR /mobile_notification
RUN touch mobile_notification/__init__.py
COPY --chown=indy:indy pyproject.toml poetry.lock README.md ./
RUN poetry install --no-dev

# --------------
FROM bcgovimages/von-image:py36-1.16-0
COPY --from=base --chown=indy:indy /home/indy/.venv /home/indy/.venv
ENV PATH="/home/indy/.venv/bin:$PATH"
WORKDIR /mobile_notification
COPY --from=base --chown=indy:indy /mobile_notification /mobile_notification

COPY int/docker/int-testing-default.yml mobile_notification
COPY int/docker/plugins-config-example.yml mobile_notification
COPY firebase_push_notification mobile_notification
ENTRYPOINT ["/bin/bash", "-c", "aca-py \"$@\"", "--"]
CMD ["start", "--arg-file", "int-testing-default.yml"]