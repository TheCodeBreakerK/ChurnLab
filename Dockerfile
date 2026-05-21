ARG BUILD_BASE_IMAGE="python:3.14-slim"
FROM --platform=$BUILDPLATFORM ${BUILD_BASE_IMAGE} AS base

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
    PATH="/root/.local/bin:$PATH"