FROM python:3.10

RUN mkdir /root/bestplace

WORKDIR /root/bestplace

COPY Pipfile Pipfile.lock main.py schemas.py geoaggr.py ./

RUN mkdir ./data

COPY ./data ./data/

RUN pip install pipenv

RUN pipenv install --system --deploy --dev

EXPOSE 8000

ENTRYPOINT ["python", "main.py", "0.0.0.0"]
