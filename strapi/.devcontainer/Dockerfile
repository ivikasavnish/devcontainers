FROM node:20-slim

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    git curl build-essential python3 zsh vim postgresql-client \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

USER node
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

USER root
RUN npm install -g npm@latest @strapi/strapi

WORKDIR /workspace
