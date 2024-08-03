FROM python:3.12-slim

RUN mkdir code
WORKDIR code/"Dialogs and moves"/


ADD . /code/

ADD requirements.txt .

RUN pip install --no-cache -r requirements.txt

CMD python main.py
