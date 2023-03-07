FROM python:3.10-slim

WORKDIR /api

COPY ./app app
COPY ./requirements.txt requirements.txt


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-setuptools \
    wget


RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
RUN bash miniconda.sh -b -p ./miniconda/
ENV PATH="/api/miniconda/bin:${PATH}"
#RUN conda init bash
#RUN bash
SHELL ["/api/miniconda/bin/conda", "run", "-n", "base", "/bin/bash", "-c"]

RUN /api/miniconda/bin/conda install -c control-toolbox -c conda-forge nutopy -y
RUN /api/miniconda/bin/conda install cmake -y
RUN /api/miniconda/bin/conda install gfortran_linux-64 -y
RUN /api/miniconda/bin/conda install scipy -y

WORKDIR /api/app/smith
RUN python setup.py build
RUN python setup.py install
RUN python -c "import smith"

WORKDIR /api

RUN python3 -m pip install -r requirements.txt

RUN python -c "import fastapi"

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
