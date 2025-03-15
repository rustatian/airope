FROM python:3.13-alpine

RUN apk add --no-cache gcc musl-dev python3-dev
RUN pip install uv
WORKDIR /app
COPY . .
RUN uv pip install --system -e .

CMD ["python", "-m", "airope"]