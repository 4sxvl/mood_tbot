FROM python:3.14-slim

WORKDIR app

COPY README.md ./
COPY pyproject.toml ./
COPY app ./

RUN pip install --no-cache-dir -e .

CMD ["python", "main.py"]
