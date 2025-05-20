FROM python:3.11
WORKDIR /src
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-distutils
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/app.py"]
