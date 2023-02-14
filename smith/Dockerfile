FROM continuumio/miniconda3

WORKDIR /smith
COPY . .

RUN conda env create -f pkg/env/smith-env-linux.yaml
SHELL ["conda", "run", "-n", "smith-dev", "/bin/bash", "-c"]
RUN python setup.py build
RUN python setup.py install
RUN echo "This is a test"
RUN python -c "import smith"
RUN python -c "import numpy"


ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "smith-dev"]
CMD ["python3", "src/smith/main.py"]

# CMD /bin/bash
