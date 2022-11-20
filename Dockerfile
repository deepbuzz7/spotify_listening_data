# First-time build can take upto 10 mins.

FROM apache/airflow:2.4.2

ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONPATH=/opt/airflow
USER root
RUN apt-get update -qq && apt-get install vim -qqq && apt-get install wget
RUN mkdir code
USER $AIRFLOW_UID
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER root
# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR $AIRFLOW_HOME


USER $AIRFLOW_UID
