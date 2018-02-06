FROM python:3.6.4-jessie
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . /usr/local/opentrons
RUN pip install /usr/local/opentrons
