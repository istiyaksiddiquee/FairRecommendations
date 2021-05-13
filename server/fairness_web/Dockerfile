FROM python:3.9

ENV PYTHONUNBUFFERED=1

ENV HOME /root

RUN apt-get update \
    && apt-get -yq install gcc build-essential zlib1g-dev wget

# Build HDF5
RUN cd ; wget https://support.hdfgroup.org/ftp/HDF5/prev-releases/hdf5-1.10/hdf5-1.10.1/src/hdf5-1.10.1.tar.gz \
    && cd ; tar zxf hdf5-1.10.1.tar.gz \
    && cd ; mv hdf5-1.10.1 hdf5-setup \
    && cd ; cd hdf5-setup ; ./configure --prefix=/usr/local/ \
    && cd ; cd hdf5-setup ; make && make install \
    && cd ; rm -rf hdf5-setup \
    && apt-get -yq autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# RUN pip install numpy pandas bottleneck tables
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/