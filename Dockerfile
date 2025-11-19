FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# Install Allure CLI
RUN curl -o allure.zip -Ls https://github.com/allure-framework/allure2/releases/download/2.28.0/allure-2.28.0.zip \
    && unzip allure.zip -d /opt/ \
    && mv /opt/allure-2.28.0 /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/bin/allure \
    && rm allure.zip

# Install Playwright + browsers
RUN pip install playwright && playwright install --with-deps

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["pytest", "--alluredir=allure-results"]
