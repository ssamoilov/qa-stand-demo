# Используем Python образ
FROM mcr.microsoft.com/devcontainers/python:3.11

# Устанавливаем Docker (для возможности запускать контейнеры внутри Codespace)
RUN apt-get update && apt-get install -y \
    docker.io \
    docker-compose \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python пакеты для тестов
RUN pip install pytest requests

# Устанавливаем GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh

# Рабочая директория
WORKDIR /workspace

# Команда по умолчанию
CMD ["sleep", "infinity"]