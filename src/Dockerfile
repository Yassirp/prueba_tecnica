FROM python:3.11
WORKDIR /src
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-distutils
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "uvicorn app.main:app --host ${HOST_IP:-0.0.0.0} --port ${HOST_PORT:-8000} --reload"]
