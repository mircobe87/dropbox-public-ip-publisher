FROM python:3.6-alpine
WORKDIR /app
COPY src/ ./
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-u", "main.py"]