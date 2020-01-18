FROM python:3.7.6-slim-buster

WORKDIR /app

COPY ./producers/requirements.txt /app/

RUN pip install -r requirements.txt

COPY producers/ /app/producers/
COPY shared_helpers/ /app/producers/shared_helpers/

CMD python producers/wait_for_dependencies.py && python producers/simulation.py
