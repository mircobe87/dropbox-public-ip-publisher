FROM python:3.6-alpine
ARG api_key_file=api_key
ARG api_secret_file=api_secret
WORKDIR /app
COPY src/ ./
RUN pip install -r requirements.txt
COPY ${api_key_file} /tmp/api_key
COPY ${api_secret_file} /tmp/api_secret
ENTRYPOINT ["python", "-u", "main.py"]