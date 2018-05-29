FROM informaticsmatters/rdkit-python-debian:Release_2018_03_01
ADD requirements.txt requirements.txt
USER root
RUN pip install -r requirements.txt
ADD . /usr/local/opentrons
RUN pip install /usr/local/opentrons
