FROM python:3.14.3-slim@sha256:6a27522252aef8432841f224d9baaa6e9fce07b07584154fa0b9a96603af7456

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHON_COLORS=0

WORKDIR /app

COPY .. /app/

RUN pip install --no-cache-dir --root-user-action ignore --upgrade pip \
    && pip install --no-cache-dir --root-user-action ignore -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["./backend/entrypoint.sh"]