FROM quay.io/fedora/fedora:42-x86_64

# install system packages
RUN dnf update -y && dnf install -y --setopt=tsflags=nodocs \
    python3-pip \
    && dnf clean all

# install application dependencies
RUN pip3 install fastapi requests uvicorn

# setup serverless user
ARG USER=serverless
ARG UID=10000
ARG HOME_DIR=/home/serverless

# create non-root user that is member of the root group
RUN adduser -lms /bin/bash -u ${UID} -g 0 ${USER} \
    && chmod -R g+rwx ${HOME_DIR}

WORKDIR ${HOME_DIR}

# install the code
COPY app app

# expose the API port
EXPOSE 8000
# expose the Worker port
EXPOSE 8080

# run as serverless
USER ${UID}

