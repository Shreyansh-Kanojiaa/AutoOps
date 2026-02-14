FROM python:3.12-slim

WORKDIR /app

COPY agent/ /app/agent/

ENV AUTOOPS_HOST=0.0.0.0
ENV AUTOOPS_PORT=8000

EXPOSE 8000

CMD ["python", "agent/main.py"]
