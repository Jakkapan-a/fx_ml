FROM python:3.12-alpine3.21
WORKDIR /app

RUN apk add --no-cache gcc musl-dev g++ cmake make libstdc++

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Migration
#RUN falsk db init
#RUN flask db migrate -m "Initial migration."
#RUN flask db upgrade

EXPOSE 5000

CMD ["python", "server.py"]