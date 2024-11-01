FROM mcr.microsoft.com/playwright:v1.48.1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt update && apt install -y ffmpeg

WORKDIR /app
COPY . /app

RUN uv tool install playwright && uv tool run playwright install

RUN uv sync

CMD ["uv", "run", "app"]