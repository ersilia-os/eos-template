FROM bentoml/model-server:0.11.0-py37

RUN conda install -c conda-forge rdkit=2020.03
RUN pip install joblib==1.1.0

WORKDIR /repo
COPY . /repo