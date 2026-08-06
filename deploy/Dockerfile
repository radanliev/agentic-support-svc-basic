FROM python:3.11-slim
WORKDIR /srv
COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock
COPY app/ app/
COPY fixtures/ fixtures/
CMD ["python", "-m", "app.agent"]
