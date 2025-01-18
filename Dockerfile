# Set environment variables
ARG EXTENSION_ID='pljbjcehnhcnofmkdbjolghdcjnmekia'
ARG EXTENSION_URL='https://bless.network/dashboard'

# Base stage for building the image
FROM debian:11-slim AS base

ARG EXTENSION_ID
ARG EXTENSION_URL

# Set environment variables
ENV EXTENSION_ID=$EXTENSION_ID
ENV EXTENSION_URL=$EXTENSION_URL

ENV GIT_USERNAME=warren-bank
ENV GIT_REPO=chrome-extension-downloader

# Install necessary packages and clean up
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

# Runtime stage
FROM debian:11-slim AS runtime

ARG EXTENSION_ID
ARG EXTENSION_URL

# Set environment variables
ENV EXTENSION_ID=${EXTENSION_ID}
ENV EXTENSION_URL=${EXTENSION_URL}

# Install necessary runtime packages
RUN apt update && \
    apt upgrade -y && \
    apt install -qqy \
    curl \
    wget \
    chromium \
    chromium-driver \
    python3 \
    python3-pip \
    python3-requests \
    python3-selenium \
    coreutils \
    bash && \
    apt autoremove --purge -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the extension and Python script
COPY --from=base /${EXTENSION_ID}.crx ./
COPY main.py ./

# Install Python packages
RUN pip3 install distro

# Default command
ENTRYPOINT ["python3", "main.py"]
