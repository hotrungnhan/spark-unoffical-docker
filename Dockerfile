
# Set environment variables
ARG EXTENSION_ID='pljbjcehnhcnofmkdbjolghdcjnmekia'
ARG EXTENSION_URL='https://bless.network/dashboard'

FROM debian:11-slim AS base

ARG EXTENSION_ID
ARG EXTENSION_URL

# Set environment variables
ENV EXTENSION_ID=$EXTENSION_ID
ENV EXTENSION_URL=$EXTENSION_URL

ENV GIT_USERNAME=warren-bank
ENV GIT_REPO=chrome-extension-downloader

# Install necessary packages in the base stage and clean up to reduce image size
RUN apt update && \
    apt upgrade -y && \
    apt install -qqy \
    curl \
    wget \
    git \
    coreutils \
    bash && \
    apt autoremove --purge -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Clone the CRX downloader repository
RUN git clone "https://github.com/${GIT_USERNAME}/${GIT_REPO}.git" && \
    chmod +x ./${GIT_REPO}/bin/*

# Download the extension
RUN ./${GIT_REPO}/bin/crxdl $EXTENSION_ID

# Create a lightweight runtime image
FROM debian:11-slim AS runtime

ARG EXTENSION_ID
ARG EXTENSION_URL
# Set environment variables
ENV EXTENSION_ID=${EXTENSION_ID}
ENV EXTENSION_URL=${EXTENSION_URL}

RUN apt update && \
    apt upgrade -y && \
    apt install -qqy \
    curl \
    wget \
    chromium \
    chromium-driver \
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
COPY --from=base /${EXTENSION_ID}.crx .
COPY main.py .

# Install Python packages required at runtime
RUN pip3 install distro

# Run the Python script
ENTRYPOINT [ "python3", "main.py" ]
