FROM python:3.12-alpine3.21
WORKDIR /app

RUN apk add --no-cache gcc musl-dev g++ cmake make libstdc++

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "server.py"]