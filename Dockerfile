FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install system dependencies
RUN apt-get update \
    && apt-get -y install gcc make \
    && rm -rf /var/lib/apt/lists/*s

#API env variables
ENV ENVIRONMENT="development"
ENV SQL_ALCHEMY_DATABASE_URL="sqlite:///.././sql_app.db"
ENV ACCESS_TOKEN_EXPIRE_MINUTES=10
ENV REFRESH_TOKEN_EXPIRE_MINUTES=30
ENV API_DISABLE_DOC=Fasle
ENV API_DEBUG=True

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt
MAINTAINER Bastien_B
EXPOSE 5010
COPY app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5010"]
