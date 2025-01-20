
ARG EXTENSION_ID='jlpniknnodfkbmbgkjelcailjljlecch'
ARG WEB_URL='https://sparkchain.ai/dashboard'

FROM debian:11-slim AS base 

ARG EXTENSION_ID
ARG WEB_URL

# Set environment variables
ENV EXTENSION_ID=$EXTENSION_ID
ENV WEB_URL=$WEB_URL

FROM base AS downloader

ENV GIT_USERNAME="sryze"
ENV GIT_REPO="crx-dl"

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
    

    WORKDIR /app

RUN git clone "https://github.com/${GIT_USERNAME}/${GIT_REPO}.git"

RUN python3 ./$GIT_REPO/crx-dl.py "${EXTENSION_ID}"

FROM base

WORKDIR /app

RUN apt update && \
    apt upgrade -y && \
    apt install -qqy \
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
    
COPY --from=downloader /app/"${EXTENSION_ID}.crx" .

COPY main.py .

RUN pip3 install distro selenium 

# Run the Python script
ENTRYPOINT [ "python3", "main.py" ]
