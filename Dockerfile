FROM jupyter/scipy-notebook:latest
LABEL version="1.1"
RUN conda update -n base conda;
RUN pip install nbgitpuller
RUN conda install -c anaconda nb_conda_kernels;
COPY ./environment.yml ./environment.yml
RUN conda env create --name py37 -f environment.yml;



