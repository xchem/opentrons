FROM informaticsmatters/rdkit:Release_2017_03_3
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . /usr/local/opentrons
RUN pip install /usr/local/opentrons