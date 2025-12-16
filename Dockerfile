FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    default-jre \
    git \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# IMPORTANT: Set browser path BEFORE installing playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PYTHONUNBUFFERED=1

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Install Allure CLI
RUN curl -o allure.zip -Ls https://github.com/allure-framework/allure2/releases/download/2.28.0/allure-2.28.0.zip \
    && unzip allure.zip -d /opt/ \
    && mv /opt/allure-2.28.0 /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/bin/allure \
    && rm allure.zip

# Copy application code
COPY . .
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "scripts.test_runner_api:app", "--host", "0.0.0.0", "--port", "8000"]
