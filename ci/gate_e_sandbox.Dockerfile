# Ephemeral GitHub-hosted CI image. Contains PUBLIC reviewed source only.
# CI runtime is network-disabled and resource-bounded; bwrap remains mandatory.
FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONNOUSERSITE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    bash bubblewrap git nodejs python3 ca-certificates && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY . /workspace
RUN python -m pip install --no-cache-dir -e '.[test]'
CMD ["python","-m","pytest","-q"]
