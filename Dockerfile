FROM python:3.11.2-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

FROM python:3.11.2-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr

ENV PATH=/root/.local/bin:$PATH
COPY --from=builder /root/.local /root/.local

COPY . .

ENTRYPOINT [ "./entrypoint.sh" ]