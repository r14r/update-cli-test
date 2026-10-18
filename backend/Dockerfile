FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN python -m pip install -q --no-cache-dir -r requirements.txt
COPY backend/app /app/app
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --retries=8 CMD python -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:8000/api/health", timeout=2)'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
