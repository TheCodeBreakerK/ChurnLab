ARG BUILD_BASE_IMAGE="nvidia/cuda:12.9.2-cudnn-runtime-ubuntu24.04"
FROM ${BUILD_BASE_IMAGE}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        git \
        build-essential \
        libgomp1 \
        fonts-cmu \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="$VIRTUAL_ENV/bin:$PATH"

RUN uv python install 3.14 && \
    uv venv /opt/venv --python 3.14

WORKDIR /workspace

CMD ["streamlit", "run", "/workspace/app.py", "--server.port=8501", "--server.address=0.0.0.0"]