

FROM debian:11-slim AS base
# Set environment variables
ARG EXTENSION_ID='pljbjcehnhcnofmkdbjolghdcjnmekia'
ARG EXTENSION_URL='https://bless.network/dashboard'

ENV EXTENSION_ID=$EXTENSION_ID
ENV EXTENSION_URL=$EXTENSION_URL

ENV GIT_USERNAME="warren-bank"
ENV GIT_REPO="chrome-extension-downloader"

RUN apt update && \
    apt upgrade -y && \
    apt install -qqy \
    curl \
    wget \
    git \
    chromium \
    chromium-driver \
    python3\ 
    python3-pip \
    python3-requests \
    python3-selenium \
    coreutils \
    bash && \
    apt autoremove --purge -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
    
# Copy the Python script and extension
WORKDIR /app


# Clone the CRX downloader repository
# RUN git clone "https://github.com/${GIT_USERNAME}/${GIT_REPO}.git" && \
#     chmod +x ./${GIT_REPO}/bin/*

# Download the extension
# RUN ./${GIT_REPO}/bin/crxdl $EXTENSION_ID

# TODO Replace with downloader
COPY pljbjcehnhcnofmkdbjolghdcjnmekia.crx .
COPY main.py .

# Install Python packages required at runtime
RUN pip3 install distro

# Run the Python script
ENTRYPOINT [ "python3", "main.py" ]
