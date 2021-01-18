FROM python:3.8-slim
WORKDIR /yasna
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py ./
CMD ["python", "main.py"]
