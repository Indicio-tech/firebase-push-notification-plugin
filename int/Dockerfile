FROM bcgovimages/von-image:py36-1.16-0 AS base

# Install and Configure Poetry
USER root
ENV POETRY_VERSION=1.1.11
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="/opt/poetry/bin:$PATH"
RUN poetry config virtualenvs.in-project true



# --------------
#FROM bcgovimages/von-image:py36-1.16-0
#COPY --from=base --chown=indy:indy /home/indy/.venv /home/indy/.venv
ENV PATH="/home/indy/.venv/bin:$PATH"

# Setup project
RUN mkdir firebase_push_notification && touch firebase_push_notification/__init__.py
COPY --chown=indy:indy pyproject.toml poetry.lock ./
COPY int/docker/int-testing-default.yml ./
COPY int/docker/plugins-config-example.yml ./
COPY firebase_push_notification firebase_push_notification
RUN poetry install --no-dev
ENTRYPOINT ["/bin/bash", "-c", "aca-py \"$@\"", "--"]
CMD ["start", "--arg-file", "int-testing-default.yml"]