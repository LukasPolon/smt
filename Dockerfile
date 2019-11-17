FROM python:3.7

COPY ./ /smt
WORKDIR /smt

RUN python setup.py install
ENV FLASK_APP /smt/app.run
