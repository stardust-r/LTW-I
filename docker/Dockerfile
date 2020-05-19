# Base image
FROM ubuntu:bionic

# Installing python and pip
RUN apt-get -y update \
    && apt-get install -y build-essential python3.6 python3-pip python3-dev

# Installing some python libraries
RUN pip3 install jupyter scipy scikit-learn

# This is the port of the container for jupyter to listen to connections
EXPOSE 8888

WORKDIR /workspace

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
