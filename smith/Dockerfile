#FROM continuumio/miniconda3
FROM continuumio/anaconda3

WORKDIR /smith
COPY . .

RUN conda env create -f pkg/env/smith-env-linux.yaml
SHELL ["conda", "run", "-n", "smith-dev", "/bin/bash", "-c"]



RUN conda init bash
ENV PATH /opt/conda/envs/smith-dev/bin:$PATH
RUN bash -c "source activate smith-dev"
RUN conda install -c control-toolbox -c conda-forge nutopy

RUN python setup.py build
RUN python setup.py install
RUN echo "This is a test"
RUN python -c "import smith"
RUN python -c "import numpy"

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "smith-dev"]
CMD ["python3", "src/smith/main.py"]

# CMD /bin/bash
